// SPDX-License-Identifier: GPL-2.0 OR BSD-2-Clause

#include <linux/errno.h>
#include <linux/init.h>
#include <linux/module.h>
#include <linux/moduleparam.h>
#include <linux/printk.h>

#include "hello1.h"

static unsigned int count = 1;
module_param(count, uint, 0444);
MODULE_PARM_DESC(count, "Number of calls to print_hello");

static int __init hello2_init(void)
{
	unsigned int i;
	int error;

	if (count > 10) {
		pr_err("count=%u is greater than 10\n", count);
		return -EINVAL;
	}

	if (count == 0 || (count >= 5 && count <= 10))
		pr_warn("count=%u is unusual; continuing\n", count);

	for (i = 0; i < count; i++) {
		error = print_hello();
		if (error)
			return error;
	}

	return 0;
}

static void __exit hello2_exit(void)
{
	pr_info("hello2 unloaded\n");
}

module_init(hello2_init);
module_exit(hello2_exit);

MODULE_AUTHOR("Artem Davydchuk");
MODULE_DESCRIPTION("Hello client with a count parameter");
MODULE_LICENSE("Dual BSD/GPL");
