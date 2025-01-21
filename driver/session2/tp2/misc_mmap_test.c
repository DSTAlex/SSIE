#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>

int main (int argc, char *argv[])
{
  char *str;
  int fd, i, ps;

  if (argc < 2) {
    fprintf (stderr,"usage: %s <devicenode>\n", argv[0]);
    return 1;
  }
 
  // open device
  if ((fd = open (argv[1], O_RDONLY)) < 0) {
    perror (argv[1]);
    exit (1);
  }

  // Get page size
  ps = getpagesize();

  printf ("page size= %d\n", ps);

  // Map memory into user space 
  str = (char *)mmap(NULL, ps, PROT_READ, MAP_PRIVATE, fd, 0);
  close (fd);
  if (str == MAP_FAILED) {
    perror ("mmap()");
    exit (1);
  };
	
  /* Display value */ 
  printf ("%s\n", str);

  /* Unmap memory */
  munmap (str, ps);

  return 0; 
}
