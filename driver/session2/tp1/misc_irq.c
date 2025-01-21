#include <linux/kernel.h> /* printk() */
#include <linux/module.h> /* modules */
#include <linux/init.h> /* module_{init,exit}() */
#include <linux/fs.h> /* file_operations */
#include <linux/uaccess.h> /* copy_{from,to}_user() */
#include <linux/miscdevice.h> /* misc driver interface */
#include <linux/sched.h>
#include <linux/workqueue.h>
#include <linux/interrupt.h> /* We want an interrupt */
#include <linux/io.h>

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Keyboard grabber driver module");
MODULE_AUTHOR("Rémi Subra <remi.subra@smile.fr>");

/*
 * Global variables
 */

#define BUF_SIZE 64
static char buffer[BUF_SIZE]; /* copy_from/to_user buffer */
static int num; // # of data to read

/* declare read wait queue */
static DECLARE_WAIT_QUEUE_HEAD(read_wait_queue);

static struct miscdevice mymisc; /* Misc device handler */

struct work_struct mywork;

static unsigned int scancode;

/* bottom-half function */
static void got_char(struct work_struct *work)
{
	scancode = inb(0x60);

	/* build read buffer with scancode data */
	sprintf(buffer, "\t%d %s\n", scancode & 0x7F,
		(scancode & 0x80 ? "Released" : "Pressed"));

	/* Set num to buffer length */
	num = strlen(buffer);

	/* wake up read */
	wake_up_interruptible(&read_wait_queue);
}

/* top half handler */
static irqreturn_t irq_handler(int irq, void *dev_id)
{
	/* Schedule the workqueue */
	schedule_work(&mywork);

	/* Don't break the keyboard ! */
	return IRQ_NONE;
}

/*
 * File operations
 */
static ssize_t misc_irq_read(struct file *file, char *buf, size_t count,
			     loff_t *ppos)
{
	int ret;

	/* Sleep until data available -> condition is '(num != 0)'  */
	ret = wait_event_interruptible(read_wait_queue, (num != 0));
	if (ret < 0) {
		pr_debug("misc_irq: woke up by signal\n");
		return -ERESTARTSYS;
	}

	/* Send scancode info to user-space */
	if (copy_to_user(buf, buffer, num))
		return -EFAULT;

	/* reset data => sleep again */
	num = 0;

	pr_info("misc_irq: send \"%s\" to user space\n", buffer);

	return strlen(buffer);
}

static int misc_irq_open(struct inode *inode, struct file *file)
{
	pr_info("misc_irq: open()\n");

	return 0;
}

static int misc_irq_release(struct inode *inode, struct file *file)
{
	pr_info("misc_irq: release()\n");

	return 0;
}

static struct file_operations misc_irq_fops = {
	.owner = THIS_MODULE,
	.read = misc_irq_read,
	.open = misc_irq_open,
	.release = misc_irq_release,
};

/*
 * Init and Exit
 */
static int __init misc_irq_init(void)
{
	int ret;

	mymisc.minor = MISC_DYNAMIC_MINOR;
	mymisc.name = "kbd_grab";
	mymisc.fops = &misc_irq_fops;

	/* Initialize misc device */
	ret = misc_register(&mymisc);
	if (ret < 0) {
		pr_warn("misc_irq: unable to get a dynamic minor\n");
		return ret;
	}

	/* Initialie workqueue */
	INIT_WORK(&mywork, got_char);

	/* Request IRQ 1 */
	void *dev_id;
	request_irq(1, irqreturn_t (*handler)(int, void *), IRQF_SHARED, "kbd_grab", dev_id);

	return ret;
}

static void __exit misc_irq_exit(void)
{
	misc_deregister(&mymisc);

	free_irq(1, irq_handler);

	pr_info("misc_irq: successfully unloaded\n");
}

module_init(misc_irq_init);
module_exit(misc_irq_exit);
