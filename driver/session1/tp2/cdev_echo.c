#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/moduleparam.h>

#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/vmalloc.h>

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Fake character driver module");
MODULE_AUTHOR("Rémi Subra <remi.subra@smile.fr>");

#define DEVICE_NAME "echo"
#define CLASS_NAME "training"

static struct class *training_class = NULL;
struct cdev cdev;
static dev_t dev_num;

const long BUFFER_SIZE = 4000 ;
char* my_buffer;
size_t index = 0;

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
	// pr_info("Dummy device read\n");
	if (index <= count)
	{
		count = index;
	}
	copy_to_user(buf, &my_buffer[index - count], count);
	index -= count;
	return count;
}

static ssize_t cfake_write(struct file *filp, const char __user *buf,
			   size_t count, loff_t *f_pos)
{
	// pr_info("Dummy device write\n");
	if (index + count >= BUFFER_SIZE)
	{
		count = BUFFER_SIZE - index - 1;
	}
	index += count;
	copy_from_user(&my_buffer[index], buf, count);

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
	int err = 0;
	int minor = 0;
	struct device *device = 0;

	pr_info("Init dummy driver\n");

	/* Request for a major and 1 minor */
	err = alloc_chrdev_region(&dev_num, minor, 1, DEVICE_NAME);
	if (err < 0) {
		pr_warn("alloc_chrdev_region() failed\n");
		return err;
	}

	/* Create device class */
	training_class = class_create(CLASS_NAME);
	if (IS_ERR(training_class)) {
		pr_warn("class_create() failed\n");
		err = PTR_ERR(training_class);
		goto err_chrdev;
	}

	/* Init cdev with file_operations */
	cdev_init(&cdev, &cfake_fops);
	cdev.owner = THIS_MODULE;

	/* Add a live char device */
	err = cdev_add(&cdev, dev_num, 1);
	if (err) {
		pr_warn("Error %d while trying to add %s%d", err, DEVICE_NAME,
			minor);
		goto err_class;
	}

	/* Create device node */
	device = device_create(training_class, NULL, /* no parent device */
			       dev_num, NULL, /* no additional data */
			       DEVICE_NAME "%d", minor);
	if (IS_ERR(device)) {
		err = PTR_ERR(device);
		pr_warn("Error %d while trying to create %s%d", err,
			DEVICE_NAME, minor);
		goto err_add;
	}

	my_buffer = vmalloc(BUFFER_SIZE);

	return 0; /* success */

err_add:
	cdev_del(&cdev);
err_class:
	class_destroy(training_class);
err_chrdev:
	unregister_chrdev_region(dev_num, 1);
	return err;
}

static void __exit cfake_exit(void)
{
	pr_info("Exit dummy module\n");

	vfree(my_buffer);
	device_destroy(training_class, dev_num);
	cdev_del(&cdev);
	class_destroy(training_class);
	unregister_chrdev_region(dev_num, 1);

	return;
}

module_init(cfake_init);
module_exit(cfake_exit);
