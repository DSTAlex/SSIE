#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/platform_device.h>

#include "platform-sample.h"

MODULE_LICENSE("GPL");

static int sample_drv_probe(struct platform_device *pdev)
{
	struct resource *res1, *res2;

	pr_info("** %s **\n", __FUNCTION__);

	res1 = platform_get_resource(pdev, IORESOURCE_MEM, 0);
	if (unlikely(!res1)) {
		pr_err("Specified resource 0 not available\n");
		return -1;
	}

	pr_info("Memory Area 1\n");
	pr_info("Start= %x,  End= %x Size= %lld\n", (unsigned int)res1->start,
		(unsigned int)res1->end, resource_size(res1));

	res2 = platform_get_resource(pdev, IORESOURCE_MEM, 1);
	if (unlikely(!res2)) {
		pr_err(" Specified resource 2 not available\n");
		return -1;
	}

	pr_info("Memory Area 2\n");
	pr_info("Start= %x,  End= %x Size= %lld\n", (unsigned int)res2->start,
		(unsigned int)res2->end, resource_size(res2));

	pr_info("IRQ Number of device= %d\n", platform_get_irq(pdev, 0));
	return 0;
}

static void sample_drv_remove(struct platform_device *pdev)
{
	printk(KERN_INFO "** %s **\n", __FUNCTION__);
}

static struct platform_driver sample_pldriver = {
  .probe          = sample_drv_probe,
  .remove         = sample_drv_remove,
  .driver = {
    .name  = DRIVER_NAME,
  },
};

static int ourinitmodule(void)
{
	pr_info("Welcome to sample platform driver !\n");
	platform_driver_register(&sample_pldriver);
	return 0;
}

static void ourcleanupmodule(void)
{
	pr_info("Exiting sample platform driver !\n");
	platform_driver_unregister(&sample_pldriver);
	return;
}

module_init(ourinitmodule);
module_exit(ourcleanupmodule);
