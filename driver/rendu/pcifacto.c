#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/init.h> /* module_{init,exit}() */
#include <linux/pci.h> /* pci_*() */
#include <linux/pci_ids.h> /* pci idents */

#include <linux/moduleparam.h>

#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/vmalloc.h>

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Factoriel character driver module");
MODULE_AUTHOR("Alexandre DI SANTO	 <alexandre.di-santo@epita.fr>");

/*
 * Supported devices VENDOR_ID/DEVICE_ID
 */

// lspci 0000:00:04:0   testdriver
// lspci -n 0000:00:04:0 1b36:0005
#define VENDOR_ID 0x1234
#define DEVICE_ID 0x11e8

#define DEVICE_NAME "edu-fact"
#define CLASS_NAME "training"

static struct class *training_class = NULL;
struct cdev cdev;
static dev_t dev_num;

static struct pci_device_id pcitest_id_table[] = {
	{ VENDOR_ID, DEVICE_ID, PCI_ANY_ID, PCI_ANY_ID, 0, 0, 0 },
	{ 0, } /* 0 terminated list */
};
MODULE_DEVICE_TABLE(pci, pcitest_id_table);

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
};

static int init_char_device()
{
    int err = 0;
	int minor = 0;
	struct device *device = 0;

	pr_info("Init char device edu-fact0\n");

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

	return 0;

err_add:
	cdev_del(&cdev);
err_class:
	class_destroy(training_class);
err_chrdev:
	unregister_chrdev_region(dev_num, 1);
	return err;
}

/*
 * PCI handling
 */
static int pcitest_probe(struct pci_dev *dev, const struct pci_device_id *ent)
{
	dev_info(&(dev->dev), "pcifacto: found %x:%x\n", ent->vendor,
		 ent->device);

	int err = init_char_device();

	return err;

}

static void pcitest_remove(struct pci_dev *dev)
{
	dev_info(&(dev->dev), "pcitest: device removed\n");
}

static struct pci_driver pcitest_driver = {
	.name = "pcifacto",
	.id_table = pcitest_id_table,
	.probe = pcitest_probe, /* Init one device */
	.remove = pcitest_remove, /* Remove one device */
};

/*
 * Init and Exit
 */
static int __init pcitest_init(void)
{
	int ret;

	/* Register PCI driver */
	ret = pci_register_driver(&pcitest_driver);
	if (ret < 0) {
		pr_warn("pcitest: unable to register PCI driver\n");
		return ret;
	}

	return 0;
}

static void __exit pcitest_exit(void)
{
	pci_unregister_driver(&pcitest_driver);
}

module_init(pcitest_init);
module_exit(pcitest_exit);
