#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/init.h> /* module_{init,exit}() */
#include <linux/pci.h> /* pci_*() */
#include <linux/pci_ids.h> /* pci idents */

MODULE_LICENSE("GPL");

/*
 * Supported devices VENDOR_ID/DEVICE_ID
 */

// lspci 0000:00:04:0   testdriver
// lspci -n 0000:00:04:0 1b36:0005
#define VENDOR_ID 0x1b36
#define DEVICE_ID 0x0005

static struct pci_device_id pcitest_id_table[] = {
	{ VENDOR_ID, DEVICE_ID, PCI_ANY_ID, PCI_ANY_ID, 0, 0, 0 },
	{ 0, } /* 0 terminated list */
};
MODULE_DEVICE_TABLE(pci, pcitest_id_table);

/*
 * PCI handling
 */
static int pcitest_probe(struct pci_dev *dev, const struct pci_device_id *ent)
{
	dev_info(&(dev->dev), "pcitest: found %x:%x\n", ent->vendor,
		 ent->device);

	return 0;
}

static void pcitest_remove(struct pci_dev *dev)
{
	dev_info(&(dev->dev), "pcitest: device removed\n");
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
