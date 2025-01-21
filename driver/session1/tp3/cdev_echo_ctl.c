#include <stdio.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

/* ioctl cmds */
#include "cdev_echo.h"

int main(int argc, char **argv)
{
	int fd, mode;
	char *dev, *cmd;

	if (argc != 3) {
		fprintf(stderr,
			"usage: %s device [reset|upper|lower|default|mode]\n",
			argv[0]);
		exit(1);
	}
	dev = argv[1];
	cmd = argv[2];

	fd = open(dev, O_RDWR);

	if (fd < 0) {
		perror("open");
		exit(1);
	}

	if (strcmp(cmd, "reset") == 0) {
		printf("reset echo buffer of %s\n", dev);
		if (ioctl(fd, CDEV_ECHO_IOCTL_RESET) < 0)
			perror("ioctl");
	} else if (strcmp(cmd, "default") == 0) {
		printf("set echo mode to default for %s\n", dev);
		if (ioctl(fd, CDEV_ECHO_IOCTL_SET_MODE,
			  CDEV_ECHO_MODE_DEFAULT) < 0)
			perror("ioctl");
	} else if (strcmp(cmd, "lower") == 0) {
		printf("set echo mode to lower for %s\n", dev);
		if (ioctl(fd, CDEV_ECHO_IOCTL_SET_MODE, CDEV_ECHO_MODE_LOWER) <
		    0)
			perror("ioctl");
	} else if (strcmp(cmd, "upper") == 0) {
		printf("set echo mode to upper for %s\n", dev);
		if (ioctl(fd, CDEV_ECHO_IOCTL_SET_MODE, CDEV_ECHO_MODE_UPPER) <
		    0)
			perror("ioctl");
	} else if (strcmp(cmd, "mode") == 0) {
		printf("get echo mode of %s\n", dev);
		if (ioctl(fd, CDEV_ECHO_IOCTL_GET_MODE, &mode) < 0)
			perror("ioctl");
		else
			printf("echo mode of %s is %d\n", dev, mode);
	} else
		fprintf(stderr, "unknown command\n");

	close(fd);

	return 0;
}
