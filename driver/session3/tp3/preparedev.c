#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/platform_device.h>

#include "platform-sample.h"

MODULE_LICENSE("GPL");

/* Specifying my resources information */
static struct resource sample_resources[] = {
	{
		.start = RESOURCE1_START_ADDRESS,
		.end = RESOURCE1_END_ADDRESS,
		.flags = IORESOURCE_MEM,
	},
	{
		.start = RESOURCE2_START_ADDRESS,
		.end = RESOURCE2_END_ADDRESS,
		.flags = IORESOURCE_MEM,
	},
	{
		.start = SAMPLE_DEV_IRQNUM,
		.end = SAMPLE_DEV_IRQNUM,
		.flags = IORESOURCE_IRQ,
	}
};

static struct platform_device sample_device = {
	.name = DRIVER_NAME,
	.id = -1,
	.num_resources = ARRAY_SIZE(sample_resources),
	.resource = sample_resources,
};

static void sample_device_release(struct device *dev)
{
	pr_info("** %s\n", __FUNCTION__);
}

static int ourinitmodule(void)
{
	pr_info("Welcome to sample Platform device !\n");
	platform_device_register(&sample_device);
	sample_device.dev.release = sample_device_release;
	return 0;
}

static void ourcleanupmodule(void)
{
	platform_device_unregister(&sample_device);
	pr_info("Exiting sample Platform (device part) !\n");
}

module_init(ourinitmodule);
module_exit(ourcleanupmodule);
