#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/moduleparam.h>

#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/uaccess.h>

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Fake character driver module");
MODULE_AUTHOR("Rémi Subra <remi.subra@smile.fr>");

#define DEVICE_NAME "echo"
#define CLASS_NAME "training"

static struct class *training_class = NULL;

static char *echo_buffer;
static struct cdev echo_cdev;
static dev_t dev_num;

/*
 * Module parameter
 */
static unsigned int buffer_size = PAGE_SIZE;
module_param(buffer_size, uint, S_IRUGO);
MODULE_PARM_DESC(buffer_size, "Size of echo buffer");

/*
 * driver functions: open, release, read, write
 */

static int cfake_open(struct inode *inode, struct file *filp)
{
	pr_info("Echo device opened\n");

	return 0;
}

static int cfake_release(struct inode *inode, struct file *filp)
{
	pr_info("Echo device released\n");

	return 0;
}

static ssize_t cfake_read(struct file *filp, char __user *buf, size_t count,
			  loff_t *f_pos)
{
	size_t i;
	char c;

	/* check for overflow */
	size_t real = min_t(loff_t, buffer_size - *f_pos, count);

	if (real)
		switch (echo_mode) {
		case CDEV_ECHO_MODE_DEFAULT:
			if (copy_to_user(buf, echo_buffer + *f_pos, real))
				return -EFAULT;
			break;
		case CDEV_ECHO_MODE_LOWER:
			for (i = 0; i < real; ++i) {
				c = echo_buffer[*f_pos + i];
				if (c > 64 && c < 91)
					c += 32;

				if (put_user(c, buf + i))
					return -EFAULT;
			}
			break;
		case CDEV_ECHO_MODE_UPPER:
			for (i = 0; i < real; ++i) {
				c = echo_buffer[*f_pos + i];
				if (c > 96 && c < 123)
					c -= 32;

				if (put_user(c, buf + i))
					return -EFAULT;
			}
			break;
		default:
			return -EFAULT;
		}

	*f_pos += real;

	return real;
}

static ssize_t cfake_write(struct file *filp, const char __user *buf,
			   size_t count, loff_t *f_pos)
{
	/* check for overflow */
	size_t real = min_t(loff_t, buffer_size - (*f_pos), count);

	if (!real)
		return -ENOMEM;

	if (copy_from_user(echo_buffer + *f_pos, buf, real))
		return -EFAULT;

	*f_pos += real;

	return real;
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

	pr_info("Init echo driver with buffer of %d\n", buffer_size);

	/* Allocate buffer */
	echo_buffer = kzalloc(buffer_size * sizeof(char), GFP_KERNEL);
	if (!echo_buffer) {
		pr_warn("kzallac failed\n");
		return -ENOMEM;
	}

	/* Request for a major and 1 minor */
	err = alloc_chrdev_region(&dev_num, minor, 1, DEVICE_NAME);
	if (err < 0) {
		pr_warn("alloc_chrdev_region() failed\n");
		goto err_alloc;
	}

	/* Create device class */
	training_class = class_create(CLASS_NAME);
	if (IS_ERR(training_class)) {
		pr_warn("class_create() failed\n");
		err = PTR_ERR(training_class);
		goto err_chrdev;
	}

	/* Init cdev with file_operations */
	cdev_init(&echo_cdev, &cfake_fops);
	echo_cdev.owner = THIS_MODULE;

	/* Add a live char device */
	err = cdev_add(&echo_cdev, dev_num, 1);
	if (err) {
		pr_warn("Error %d while trying to add %s%d", err, DEVICE_NAME,
			minor);
		goto err_class;
	}

	/* Create device node */
	device = device_create(training_class, NULL, /* no parent device */
			       dev_num, NULL, DEVICE_NAME "%d", minor);
	if (IS_ERR(device)) {
		err = PTR_ERR(device);
		pr_warn("Error %d while trying to create %s%d", err,
			DEVICE_NAME, minor);
		goto err_add;
	}

	return 0; /* success */

err_add:
	cdev_del(&echo_cdev);
err_class:
	class_destroy(training_class);
err_chrdev:
	unregister_chrdev_region(dev_num, 1);
err_alloc:
	kfree(echo_buffer);
	return err;
}

static void __exit cfake_exit(void)
{
	pr_info("Exit echo module\n");

	device_destroy(training_class, dev_num);
	cdev_del(&echo_cdev);
	class_destroy(training_class);
	unregister_chrdev_region(dev_num, 1);
	kfree(echo_buffer);
	return;
}

module_init(cfake_init);
module_exit(cfake_exit);
