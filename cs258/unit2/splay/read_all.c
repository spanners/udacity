#include <stdlib.h>
#include <sys/types.h>
#include <sys/uio.h>
#include <unistd.h>
#include <assert.h>
#include <time.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <string.h>
#include <stdio.h>
#include <errno.h>
#include <limits.h>

int MIN(int x, int y) {
	return ((x) < (y) ? (x) : (y));
}

/* fault injecting read() */
ssize_t read_fi (int fd, void *buf, size_t nbyte)
{
	nbyte = (rand() % nbyte) + 1;
	return read (fd, buf, nbyte);
}

/* keep on calling read() until the whole file is read */
ssize_t read_all (int fd, void *buf, size_t nbyte)
{
	size_t left;
	ssize_t res;

	assert (fd >= 0);
	assert (buf);

	left = nbyte;
	while (left) {
		res = read_fi (fd, buf, MIN(SSIZE_MAX, left));
		if (res == -1) {
			if (errno == EINTR) {
				continue;	/* Not an error */
			}
		}
		if ((res == -1) || (res == 0)) {
			if (nbyte != left) {
				return nbyte - left;
			}
			return res;
		}
		buf += res;
		left -= res;
	}
	return nbyte - left;
}

/* stress test the read_all() function */
int main (void)
{
	srand(time(NULL));

	int fd = open("splay.py", O_RDONLY);
	assert (fd >= 0);

	struct stat buf;
	int res = fstat (fd, &buf);
	assert (res==0);

	off_t len = buf.st_size;
	char *definitive = (char *) malloc (len);
	assert (definitive);

	res = read (fd, definitive, len);
	assert (res == len);

	int i;
	char *test = (char *) malloc (len);
	for (i=0; i<1000000; i++) {
		res = lseek (fd, 0, SEEK_SET);
		assert (res==0);
		int j;
		for (j=0; j<len; j++) {
			test[j] = rand();
		}
		res = read_all (fd, test, len);
		assert (res==len);
		assert (strncmp(test, definitive, len)==0);
	}

	return 0;
}
