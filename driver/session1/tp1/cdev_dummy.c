#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/moduleparam.h>

#include <linux/cdev.h>
#include <linux/fs.h>

#include <linux/kdev_t.h>
//#include <sys/types.h>

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Fake character driver module");
MODULE_AUTHOR("Rémi Subra <remi.subra@smile.fr>");

#define DEVICE_NAME "dummy"
#define CLASS_NAME "training"

/* global variables */
dev_t my_dev;
struct class* my_class;
static struct cdev my_cdev; 

static int major = 0;		/* default to dynamic major */
module_param(major, int, 0);
MODULE_PARM_DESC(major, "Major device number");


/*
 * driver functions: open, release, read, write
 */

static int cfake_open(struct inode *inode, struct file *filp)
{
	pr_info("Dummy device opened\n");

	return 0;
}

static int cfake_release(struct inode *inode, struct file *filp)
{
	pr_info("Dummy device released\n");

	return 0;
}

static ssize_t cfake_read(struct file *filp, char __user *buf, size_t count,
			  loff_t *f_pos)
{
	pr_info("Dummy device read\n");

	return 0;
}

static ssize_t cfake_write(struct file *filp, const char __user *buf,
			   size_t count, loff_t *f_pos)
{
	pr_info("Dummy device write\n");

	return count;
}

/* Functions declaration */

struct file_operations cfake_fops = {
	.owner = THIS_MODULE,
	.read = cfake_read,
	.write = cfake_write,
	.open = cfake_open,
	.release = cfake_release,
};

/*
 * Module entries called by insmod/rmmod
 */

static int __init cfake_init(void)
{
	pr_info("Init dummy driver\n");

	my_dev = MKDEV(major, 0);
	/* Request for a major and 1 minor */
	int err = alloc_chrdev_region(&my_dev, 0, 1, "alex_driver");
	if (err < 0)
		return err;
	/* Create device class */
	my_class = class_create(CLASS_NAME);

	/* Init cdev with file_operations */
	cdev_init(&my_cdev, &cfake_fops);
	my_cdev.owner = THIS_MODULE;

	/* Add a live char device */
	cdev_add(&my_cdev, my_dev, 1);

	/* Create device node */
	struct device* dev= device_create(my_class, NULL, my_dev, NULL, DEVICE_NAME "%d", MINOR(my_dev));

	return 0; /* success */
}

static void __exit cfake_exit(void)
{
	pr_info("Exit dummy module\n");

	device_destroy(my_class, my_dev);

	cdev_del(&my_cdev);

	//destroy class
	class_destroy(my_class);

	unregister_chrdev_region(my_dev, 1);

	return;
}

module_init(cfake_init);
module_exit(cfake_exit);
