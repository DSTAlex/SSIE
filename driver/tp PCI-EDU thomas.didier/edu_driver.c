#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/init.h>
#include <linux/pci.h>
#include <linux/pci_ids.h>
#include <linux/cdev.h>

MODULE_LICENSE("GPL");

/*
 * Supported devices VENDOR_ID/DEVICE_ID
 */

#define VENDOR_ID 0x1234
#define DEVICE_ID 0x11e8

// Device node name
#define DEVICE_NAME "edu-fact0"

static struct pci_device_id pci_id_table[] = {
	{ VENDOR_ID, DEVICE_ID, PCI_ANY_ID, PCI_ANY_ID, 0, 0, 0 },
	{
		0,
	}
};

MODULE_DEVICE_TABLE(pci, pci_id_table);

/*
 * Global variables
 */

static struct edu_device *edu_dev;

struct edu_device {
    struct pci_dev *pci_dev;
    void __iomem *base0;
    struct cdev cdev;
    dev_t devt;
};

/* 
 * EDU read and write
 */

static ssize_t edu_factorial_read(struct file *file, char __user *buf,
				  size_t count, loff_t *ppos)
{
	pr_info("edu-fact0: read invoked\n");
    unsigned int result;
    char result_str[32];
    size_t len;

    result = ioread32(edu_dev->base0 + 0x08);
    len = snprintf(result_str, sizeof(result_str), "%i\n", result);

    if (len > count) {
        pr_err("edu-fact0: not enough space in user buffer\n");
        return -EINVAL;
    }

    if (count > len - *ppos)
	count = len - *ppos;

    if (copy_to_user(buf, result_str + *ppos, count)) {
        pr_err("edu-fact0: failed to copy result to user\n");
        return -EFAULT;
    }
    *ppos += count;
    return count;
}

static ssize_t edu_factorial_write(struct file *file, const char __user *buf,
				   size_t count, loff_t *ppos)
{
	pr_info("edu-fact0: write invoked\n");
	unsigned int n;
	char n_str[32];

	if (count > sizeof(n_str)) {
		pr_err("edu-fact0: input too long\n");
		return -EINVAL;
	}
	if (copy_from_user(n_str, buf, count)) {
		pr_err("edu-fact0: failed to copy input from user\n");
		return -EFAULT;
	}

	n = simple_strtoul(n_str, NULL, 10);
	iowrite32(n, edu_dev->base0  + 0x08);

	return count;
}

/*
 * EDU probe and remove
 */
static const struct file_operations edu_fops = {
    .owner = THIS_MODULE,
    .read = edu_factorial_read,
    .write = edu_factorial_write,
};

static int edu_probe(struct pci_dev *dev, const struct pci_device_id *ent)
{
	dev_info(&(dev->dev), "edu-fact0: found %x:%x\n", ent->vendor,
		 ent->device);

	int err = 0;

	/* Alloc private data */
    edu_dev = kzalloc(sizeof(struct edu_device), GFP_KERNEL);
	if (!edu_dev) {
		dev_warn(&dev->dev, "edu-fact0: unable to alloc memory\n");
		return -ENOMEM;
	}

	/* set private data */
	edu_dev->pci_dev = dev;
	pci_set_drvdata(dev, edu_dev);

	/* enable PCI device */
	err = pci_enable_device(dev);
	if (err) {
		dev_warn(&dev->dev, "edu-fact0: unable to enable PCI device\n");
		goto err_alloc;
	}

	/* request BAR 0 */
	err = pci_request_region(dev, 0, DEVICE_NAME);
	if (err) {
		dev_warn(&dev->dev, "edu-fact0: unable to request regions\n");
		goto err_enable;
	}

	/* map BAR 0 */
	edu_dev->base0 = pci_iomap(dev, 0, pci_resource_len(dev, 0));
	if (!edu_dev->base0) {
		dev_warn(&dev->dev, "edu-fact0: unable to map BAR0\n");
		err = -EIO;
		goto err_region;
	}

    /* alloc char device numbers */
    err = alloc_chrdev_region(&edu_dev->devt, 0, 1, DEVICE_NAME);
    if (err) {
        dev_warn(&dev->dev, "edu-fact0: unable to alloc chrdev region\n");
        goto err_alloc_chrdev;
    }

    /* Init char device */
    cdev_init(&edu_dev->cdev, &edu_fops);
    edu_dev->cdev.owner = THIS_MODULE;

    err = cdev_add(&edu_dev->cdev, edu_dev->devt, 1);
    if (err) {
        dev_warn(&dev->dev, "edu-fact0: unable to add cdev\n");
        goto err_add_cdev;
	} else {
		dev_info(&dev->dev, "edu-fact0: cdev added successfully\n");
	}

	/* divice class */
	struct class *edu_class = class_create("edu_class");
	if (IS_ERR(edu_class)) {
		dev_warn(&dev->dev, "edu-fact0: unable to create class\n");
		goto err_device_create;
	}

	/* create device file */
	if (!device_create(edu_class, NULL, edu_dev->devt, NULL, DEVICE_NAME)) {
		dev_warn(&dev->dev, "edu-fact0: unable to create device file\n");
		goto err_device_create;
	}

	return 0;

err_device_create:
	class_destroy(edu_class);
err_add_cdev:
    unregister_chrdev_region(edu_dev->devt, 1);
err_alloc_chrdev:
    pci_iounmap(dev, edu_dev->base0);
err_region:
	pci_release_region(dev, 0);
err_enable:
	pci_disable_device(dev);
err_alloc:
	kfree(edu_dev);
	return err;
}

static void edu_remove(struct pci_dev *dev)
{
    dev_info(&(dev->dev), "edu-fact0: device remove\n");
    struct edu_device *edu_dev = pci_get_drvdata(dev);

    cdev_del(&edu_dev->cdev);
    unregister_chrdev_region(edu_dev->devt, 1);

    pci_iounmap(dev, edu_dev->base0);
    pci_release_region(dev, 0);
    pci_disable_device(dev);
    kfree(edu_dev);
}

static struct pci_driver edu_pci_driver = {
	.name = DEVICE_NAME,
	.id_table = pci_id_table,
	.probe = edu_probe,
	.remove = edu_remove,
};

/*
 * Init and Exit
 */
static int __init edu_init(void)
{
	int err;

	/* Register PCI driver */
	err = pci_register_driver(&edu_pci_driver);
	if (err < 0) {
		pr_warn("edu-fact0: unable to register PCI driver\n");
		return err;
	}

	return 0;
}

static void __exit edu_exit(void)
{
	pci_unregister_driver(&edu_pci_driver);
}

module_init(edu_init);
module_exit(edu_exit);
