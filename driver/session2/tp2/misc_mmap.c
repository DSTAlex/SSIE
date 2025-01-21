#include <asm/io.h>
#include <linux/fs.h>
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/miscdevice.h> /* misc driver interface */
#include <linux/mm.h>
#include <linux/module.h>
#include <linux/slab.h>

MODULE_LICENSE("GPL");

// buffer to map to user space
static char *buffer;

static struct miscdevice mymisc; /* Misc device handler */

static int misc_mmaptest_mmap(struct file *filp, struct vm_area_struct *vma)
{
	unsigned long page, pos;
	unsigned long start =
		(unsigned long)vma->vm_start; // user address to start at
	unsigned long size = (unsigned long)(vma->vm_end -
					     vma->vm_start); // size of map area

	/* start off at the start of the buffer */
	pos = (unsigned long)buffer;

	/* loop through all the physical pages in the buffer */
	/* Remember this won't work for vmalloc()d memory ! */
	while (size > 0) {
		/* get the physical address of the page corresponding to the buffer address */
		page = virt_to_phys((void *)pos);

		/* Remap address to the process's vma */
		if (remap_pfn_range(vma, start, page >> PAGE_SHIFT, PAGE_SIZE,
				    PAGE_SHARED))
			return -EAGAIN;

		start += PAGE_SIZE;
		pos += PAGE_SIZE;
		size -= PAGE_SIZE;
	}

	return 0;
}

static int misc_mmaptest_open(struct inode *inode, struct file *filp)
{
	return 0;
}

static int misc_mmaptest_release(struct inode *inode, struct file *filp)
{
	return 0;
}

/* VFS methods */
static struct file_operations misc_mmaptest_fops = {
	mmap: misc_mmaptest_mmap,
	open: misc_mmaptest_open,
	release: misc_mmaptest_release,
};

static
int __init misc_mmaptest_init(void)
{
	struct page *page;
	int ret;

	mymisc.minor = MISC_DYNAMIC_MINOR;
	mymisc.name = "mydriver_misc_mmap";
	mymisc.fops = &misc_mmaptest_fops;

	ret = misc_register(&mymisc);

	if (ret < 0) {
		pr_warn("misc_mmaptest: unable to get a dynamic minor\n");
		return ret;
	}

	// Alloc a 1 page buffer
	buffer = kzalloc(PAGE_SIZE, GFP_KERNEL);
	if (!buffer) {
		misc_deregister(&mymisc);
		return -ENOMEM;
	}

	// Reserve allocated pages
	for (page = virt_to_page(buffer);
	     page < virt_to_page(buffer + PAGE_SIZE); page++)
		SetPageReserved(page);

	/* Add something to read */
	strcpy(buffer, "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.");

	return 0;
}

static
void __exit misc_mmaptest_exit(void)
{
	struct page *page;

	for (page = virt_to_page(buffer);
	     page < virt_to_page(buffer + PAGE_SIZE); page++)
		ClearPageReserved(page);

	kfree(buffer);
	misc_deregister(&mymisc);
}

module_init(misc_mmaptest_init);
module_exit(misc_mmaptest_exit);
