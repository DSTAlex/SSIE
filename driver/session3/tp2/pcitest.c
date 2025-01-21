#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/init.h> /* module_{init,exit}() */
#include <linux/pci.h> /* pci_*() */
#include <linux/pci_ids.h> /* pci idents */

MODULE_LICENSE("GPL");

/*
 * Supported devices VENDOR_ID/DEVICE_ID
 */

#define VENDOR_ID 0x1b36
#define DEVICE_ID 0x0005

static struct pci_device_id pcitest_id_table[] = {
	{ VENDOR_ID, DEVICE_ID, PCI_ANY_ID, PCI_ANY_ID, 0, 0, 0 },
	{
		0,
	} /* 0 terminated list */
};
MODULE_DEVICE_TABLE(pci, pcitest_id_table);

/*
 * Global variables
 */
struct pcitest {
	struct pci_dev *dev;
	void __iomem *base0;
	void __iomem *base1;
};

#define TEST_WIDTH_TYPE 1
#define TEST_OFFSET 4
#define TEST_DATA 8
#define TEST_COUNT 12

/*
 * PCI handling
 */
static int pcitest_probe(struct pci_dev *dev, const struct pci_device_id *ent)
{
	struct pcitest *pdev;
	int err = 0;
	uint8_t wt;
	uint32_t data, offset;
	uint8_t n = 0;

	dev_info(&(dev->dev), "pcitest: found %x:%x\n", ent->vendor,
		 ent->device);

	/* Alloc private data */
	pdev = kzalloc(sizeof(struct pcitest), GFP_KERNEL);
	if (!pdev) {
		dev_warn(&dev->dev, "pcitest: unable to alloc memory\n");
		return -ENOMEM;
	}

	/* set private data */
	pdev->dev = dev;
	pci_set_drvdata(dev, pdev);

	/* enable device */
	err = pci_enable_device(dev);
	if (err) {
		dev_warn(&dev->dev, "pcitest: unable to enable device\n");
		goto err_alloc;
	}

	/* request regions */
	err = pci_request_regions(dev, "pcitest");
	if (err) {
		dev_warn(&dev->dev, "pcitest: unable to request regions\n");
		goto err_enable;
	}

	/* map BAR 0 */
	pdev->base0 = pci_iomap(dev, 0, pci_resource_len(dev, 0));
	if (!pdev->base0) {
		dev_warn(&dev->dev, "pcitest: unable to map BAR0\n");
		err = -EIO;
		goto err_regions;
	}

	/* map BAR 1 */
	pdev->base1 = pci_iomap(dev, 1, pci_resource_len(dev, 1));
	if (!pdev->base1) {
		dev_warn(&dev->dev, "pcitest: unable to map BAR0\n");
		err = -EIO;
		goto err_map0;
	}

	/* read test in BAR0 */
	for (n = 0; n < 256; n++) {
		iowrite8(n, pdev->base0);
		wt = ioread8(pdev->base0 + TEST_WIDTH_TYPE);
		if (!wt)
			break;
		offset = ioread32(pdev->base0 + TEST_OFFSET);
		data = ioread32(pdev->base0 + TEST_DATA);
		dev_info(
			&(dev->dev),
			"pcitest: BAR0 - n=%d - width_type=%d - offset=%d - data=%d\n",
			n, wt, offset, data);
	}

	/* read test in BAR1 */
	for (n = 0; n < 256; n++) {
		iowrite8(n, pdev->base1);
		wt = ioread8(pdev->base1 + TEST_WIDTH_TYPE);
		if (!wt)
			break;
		offset = ioread32(pdev->base1 + TEST_OFFSET);
		data = ioread32(pdev->base1 + TEST_DATA);
		dev_info(
			&(dev->dev),
			"pcitest: BAR1 - n=%d - width_type=%d - offset=%d - data=%d\n",
			n, wt, offset, data);
	}

	return 0;

err_map0:
	pci_iounmap(dev, pdev->base0);
err_regions:
	pci_release_regions(dev);
err_enable:
	pci_disable_device(dev);
err_alloc:
	kfree(pdev);
	return err;
}

static void pcitest_remove(struct pci_dev *dev)
{
	struct pcitest *pdev = pci_get_drvdata(dev);

	dev_info(&(dev->dev), "pcitest: device removed\n");

	/* release all resources */
	pci_iounmap (dev, pdev->base0);
	pci_iounmap (dev, pdev->base1);
	pci_release_regions(dev);
	pci_disable_device(dev);
	kfree(pdev);

}

static struct pci_driver pcitest_driver = {
	.name = "pcitest",
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
