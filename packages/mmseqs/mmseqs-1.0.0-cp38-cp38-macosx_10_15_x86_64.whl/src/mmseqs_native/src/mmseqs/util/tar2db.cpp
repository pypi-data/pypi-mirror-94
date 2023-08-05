#include <mmseqs/commons/dBWriter.h>
#include <mmseqs/output.h>
#include <mmseqs/commons/fileUtil.h>
#include <mmseqs/commons/patternCompiler.h>
#include <mmseqs/commons/util.h>

#include "microtar.h"
#include <mmseqs/output.h>

#ifdef OPENMP
#include <omp.h>
#endif

#ifdef HAVE_ZLIB
#include <zlib.h>
static int file_gzread(mtar_t *tar, void *data, size_t size) {
  size_t res = gzread((gzFile)tar->stream, data, size);
  return (res == size) ? MTAR_ESUCCESS : MTAR_EREADFAIL;
}

static int file_gzseek(mtar_t *tar, long offset, int whence) {
  int res = gzseek((gzFile)tar->stream, offset, whence);
  return (res != -1) ? MTAR_ESUCCESS : MTAR_ESEEKFAIL;
}

static int file_gzclose(mtar_t *tar) {
  gzclose((gzFile)tar->stream);
  return MTAR_ESUCCESS;
}

int mtar_gzopen(mtar_t *tar, const char *filename) {
  // Init tar struct and functions
  memset(tar, 0, sizeof(*tar));
  tar->read = file_gzread;
  tar->seek = file_gzseek;
  tar->close = file_gzclose;
  tar->isFinished = 0;
  // Open file
  tar->stream = gzopen(filename, "rb");
  if (!tar->stream) {
    return MTAR_EOPENFAIL;
  }

  // Return ok
  return MTAR_ESUCCESS;
}
#endif

#ifdef HAVE_BZLIB
#include <bzlib.h>
#endif

int tar2db(mmseqs_output *out, Parameters &par) {
  //    Parameters &par = Parameters::getInstance();
  //    par.parseParameters(argc, argv, command, true,
  //    Parameters::PARSE_VARIADIC, 0);

  std::vector<std::string> filenames(par.filenames);
  for (size_t i = 0; i < filenames.size(); i++) {
    if (FileUtil::directoryExists(out, filenames[i].c_str()) == true) {
      out->failure("File {} is a directory", filenames[i] );
    }
  }

  PatternCompiler include(out, par.tarInclude.c_str());
  PatternCompiler exclude(out, par.tarExclude.c_str());

  std::string dataFile = filenames.back();
  filenames.pop_back();
  std::string indexFile = dataFile + ".index";

  std::string sourceFile = dataFile + ".source";
  FILE *source = FileUtil::openAndDelete(out, sourceFile.c_str(), "w");

  std::string lookupFile = dataFile + ".lookup";
  FILE *lookup = FileUtil::openAndDelete(out, lookupFile.c_str(), "w");

  DBWriter writer(out, dataFile.c_str(), indexFile.c_str(), par.threads,
                  par.compressed, par.outputDbType);
  writer.open();
  Log::Progress progress;
  char buffer[4096];

  size_t globalKey = 0;
  for (size_t i = 0; i < filenames.size(); i++) {
    size_t len = snprintf(buffer, sizeof(buffer), "%zu\t%s\n", i,
                          FileUtil::baseName(out, filenames[i]).c_str());
    int written = fwrite(buffer, sizeof(char), len, source);
    if (written != (int)len) {
      out->failure("Cannot write to source file {}", sourceFile);
    }

    mtar_t tar;
    if (Util::endsWith(".tar.gz", filenames[i]) ||
        Util::endsWith(".tgz", filenames[i])) {
#ifdef HAVE_ZLIB
      if (mtar_gzopen(&tar, filenames[i].c_str()) != MTAR_ESUCCESS) {
        out->failure("Cannot open file {}", filenames[i] );
      }
#else
      out->failure("MMseqs2 was not compiled with zlib support. Cannot read compressed input");
#endif
    } else {
      if (mtar_open(&tar, filenames[i].c_str()) != MTAR_ESUCCESS) {
        out->failure("Cannot open file {}", filenames[i] );
      }
    }

#pragma omp parallel shared(tar, buffer)
    {
      size_t bufferSize = 10 * 1024;
      char *dataBuffer = (char *)malloc(bufferSize);
      size_t inflateSize = 10 * 1024;
      char *inflateBuffer = (char *)malloc(inflateSize);
      mtar_header_t header;
      size_t currentKey = 0;
#ifdef HAVE_ZLIB
      const unsigned int CHUNK = 128 * 1024;
      unsigned char in[CHUNK];
      unsigned char out_chunk[CHUNK];
      z_stream strm;
      memset(&strm, 0, sizeof(z_stream));
      strm.zalloc = Z_NULL;
      strm.zfree = Z_NULL;
      strm.opaque = Z_NULL;
      strm.next_in = in;
      strm.avail_in = 0;
      int status = inflateInit2(&strm, 15 | 32);
      if (status < 0) {
        out->failure("Cannot initialize zlib stream");
      }
#endif
      unsigned int thread_idx = 0;
#ifdef OPENMP
      thread_idx = static_cast<unsigned int>(omp_get_thread_num());
#endif
      bool proceed = true;
      while (proceed) {
        bool writeEntry = true;
#pragma omp critical
        {
          if (tar.isFinished == 0 &&
              (mtar_read_header(&tar, &header)) != MTAR_ENULLRECORD) {
            if (header.type == MTAR_TREG) {
              progress.updateProgress();
              if (include.isMatch(header.name) == false ||
                  exclude.isMatch(header.name) == true) {
                __sync_fetch_and_add(&(globalKey), 1);
                writeEntry = false;
              } else {
                if (header.size > bufferSize) {
                  bufferSize = header.size * 1.5;
                  dataBuffer = (char *)realloc(dataBuffer, bufferSize);
                }
                if (mtar_read_data(&tar, dataBuffer, header.size) !=
                    MTAR_ESUCCESS) {
                  out->failure("Cannot read entry {}", header.name );
                }
                proceed = true;
                currentKey = __sync_fetch_and_add(&(globalKey), 1);

                size_t len = snprintf(
                    buffer, sizeof(buffer), "%zu\t%s\t%zu\n", currentKey,
                    FileUtil::baseName(out, header.name).c_str(), i);
                int written = fwrite(buffer, sizeof(char), len, lookup);
                if (written != (int)len) {
                  out->failure("Cannot write to lookup file {}", lookupFile);
                }
              }
            } else {
              proceed = false;
              writeEntry = false;
            }
          } else {
            tar.isFinished = 1;
            proceed = false;
            writeEntry = false;
          }
        }
        if (proceed && writeEntry) {
          if (Util::endsWith(".gz", header.name)) {
#ifdef HAVE_ZLIB
            inflateReset(&strm);
            writer.writeStart(thread_idx);
            strm.avail_in = header.size;
            strm.next_in = (unsigned char *)dataBuffer;
            do {
              unsigned have;
              strm.avail_out = CHUNK;
              strm.next_out = out_chunk;
              int err = inflate(&strm, Z_NO_FLUSH);
              switch (err) {
                case Z_OK:
                case Z_STREAM_END:
                case Z_BUF_ERROR:
                  break;
                default:
                  inflateEnd(&strm);
                  out->failure("Gzip error {} entry {}", err, header.name);
              }
              have = CHUNK - strm.avail_out;
              writer.writeAdd((const char *)out_chunk, have, thread_idx);
            } while (strm.avail_out == 0);
            writer.writeEnd(currentKey, thread_idx);
#else
            out->failure("MMseqs2 was not compiled with zlib support. Cannot read compressed input");
#endif
          } else if (Util::endsWith(".bz2", header.name)) {
#ifdef HAVE_BZLIB
            unsigned int entrySize = inflateSize;
            int err;
            while ((err = BZ2_bzBuffToBuffDecompress(inflateBuffer, &entrySize,
                                                     dataBuffer, header.size, 0,
                                                     0) == BZ_OUTBUFF_FULL)) {
              entrySize = inflateSize = inflateSize * 1.5;
              inflateBuffer = (char *)realloc(inflateBuffer, inflateSize);
            }
            if (err != BZ_OK) {
              out->failure("Could not decompress {}", header.name);
            }
            writer.writeData(inflateBuffer, entrySize, currentKey, thread_idx);
#else
            out->failure("MMseqs2 was not compiled with bzlib support. Cannot read compressed input");
#endif
          } else {
            writer.writeData(dataBuffer, header.size, currentKey, thread_idx);
          }
        }
      }

#ifdef HAVE_ZLIB
      inflateEnd(&strm);
#endif
      free(inflateBuffer);
      free(dataBuffer);
    }  // end omp

    mtar_close(&tar);
  }  // filename for
  writer.close();
  if (fclose(lookup) != 0) {
    out->failure("Cannot close file {}", lookupFile);
  }
  if (fclose(source) != 0) {
    out->failure("Cannot close file {}", sourceFile);
  }

  return EXIT_SUCCESS;
}
