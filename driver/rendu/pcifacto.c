
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/init.h> /* module_{init,exit}() */
#include <linux/pci.h> /* pci_*() */
#include <linux/pci_ids.h> /* pci idents */

#include <linux/moduleparam.h>

#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/vmalloc.h>

#define VENDOR_ID 0x1234
#define DEVICE_ID 0x11e8

#define DEVICE_NAME "edu-fact"
#define CLASS_NAME "training"

#define BUFFER_SIZE 32

static struct class *training_class = NULL;
struct cdev cdev;
static dev_t dev_num;

struct pcifacto {
	struct pci_dev *dev;
	void __iomem *base0;
};

struct pcifacto *pdev;

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Factoriel character driver module");
MODULE_AUTHOR("Alexandre DI SANTO	 <alexandre.di-santo@epita.fr>");




static struct pci_device_id pcifacto_id_table[] = {
	{ VENDOR_ID, DEVICE_ID, PCI_ANY_ID, PCI_ANY_ID, 0, 0, 0 },
	{ 0, } /* 0 terminated list */
};
MODULE_DEVICE_TABLE(pci, pcifacto_id_table);

struct eduv7_priv {
    u8 __iomem *mem;
};

static ssize_t facto_read(struct file *filp, char __user *buf, size_t count,
			  loff_t *f_pos)
{
	pr_info("Dummy device read\n");
	unsigned int data;
	char n_str[BUFFER_SIZE];

	size_t real = min_t(loff_t, BUFFER_SIZE - *f_pos, count);

	data = ioread32(pdev->base0 + 0x08);
	size_t len = snprintf(n_str, sizeof(n_str), "%i\n", data);

	if (len > count) {
        pr_err("pcifacto: buffer to small\n");
        return -EINVAL;
    }

	if (real)
	{
		if (copy_to_user(buf, n_str + *f_pos, real))
		{
			pr_err("pcifacto: read error\n");
			return -EFAULT;
		}
	}

	*f_pos += real;
	return real;
}

static ssize_t facto_write(struct file *filp, const char __user *buf,
			   size_t count, loff_t *f_pos)
{
	pr_info("Dummy device write\n");
	char n_str[BUFFER_SIZE];

	size_t real = min_t(loff_t, BUFFER_SIZE - *f_pos, count);

	if (!real)
	{
		pr_err("pcifacto: error in write\n");
		return -ENOMEM;
	}

	if (copy_from_user(n_str, buf, count)) {
		pr_err("pcifacto: write failed in copy\n");
		return -EFAULT;
	}

	unsigned int truc = simple_strtoul(n_str, NULL, 10);
	iowrite32(truc, pdev->base0  + 0x08);

	return count;
}

/* Functions declaration */
struct file_operations cfake_fops = {
	.owner = THIS_MODULE,
	.read = facto_read,
	.write = facto_write,
};

static int init_char_device(void)
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
			       DEVICE_NAME "%d", 0);
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
static int pcifacto_probe(struct pci_dev *dev, const struct pci_device_id *ent)
{
	int err = 0;

	dev_info(&(dev->dev), "pcifacto: found %x:%x\n", ent->vendor,
		 ent->device);


	dev_info(&(dev->dev), "etape 1\n");
	/* Alloc private data */
	pdev = kzalloc(sizeof(struct pcifacto), GFP_KERNEL);
	if (!pdev) {
		dev_warn(&dev->dev, "pcitest: unable to alloc memory\n");
		return -ENOMEM;
	}

	/* set private data */
	pdev->dev = dev;
	pci_set_drvdata(dev, pdev);

	dev_info(&(dev->dev), "etape 2\n");
	/* enable device */
	err = pci_enable_device(dev);
	if (err) {
		dev_warn(&dev->dev, "pcitest: unable to enable device\n");
		goto err_alloc;
	}

	dev_info(&(dev->dev), "etape 3\n");

	/* request regions */
	err = pci_request_regions(dev, DEVICE_NAME);


	dev_info(&(dev->dev), "etape 3.5\n");

	if (err) {
		dev_warn(&dev->dev, "pcitest: unable to request regions\n");
		goto err_enable;
	}

	dev_info(&(dev->dev),"etape 4\n");
	/* map BAR 0 */
	pdev->base0 = pci_iomap(dev, 0, pci_resource_len(dev, 0));
	if (!pdev->base0) {
		dev_warn(&dev->dev, "pcitest: unable to map BAR0\n");
		err = -EIO;
		goto err_regions;
	}

	return 0;

err_regions:
	pci_release_regions(dev);
err_enable:
	pci_disable_device(dev);
err_alloc:
	kfree(pdev);
	return err;

}

static void pcifacto_remove(struct pci_dev *dev)
{

	//struct pcitest *pdev = pci_get_drvdata(dev);

	dev_info(&(dev->dev), "pcifacto: device removed\n");

	pci_iounmap (dev, pdev->base0);
	pci_release_regions(dev);
	pci_disable_device(dev);
	kfree(pdev);
}

static struct pci_driver pcifacto_driver = {
	.name = "pcifacto",
	.id_table = pcifacto_id_table,
	.probe = pcifacto_probe, /* Init one device */
	.remove = pcifacto_remove, /* Remove one device */
};

/*
 * Init and Exit
 */
static int __init pcifacto_init(void)
{
	int ret;

	/* Register PCI driver */
	ret = pci_register_driver(&pcifacto_driver);
	if (ret < 0) {
		pr_warn("pcifacto: unable to register PCI driver\n");
		return ret;
	}

	ret = init_char_device();
	if (ret < 0) {
		pr_warn("pcifacto: unable to create device\n");
		return ret;
	}

	return 0;
}

static void __exit pcifacto_exit(void)
{

	pci_unregister_driver(&pcifacto_driver);

	device_destroy(training_class, dev_num);
	cdev_del(&cdev);
	class_destroy(training_class);
	unregister_chrdev_region(dev_num, 1);
}

module_init(pcifacto_init);
module_exit(pcifacto_exit);
