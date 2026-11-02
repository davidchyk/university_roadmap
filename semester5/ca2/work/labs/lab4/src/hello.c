// SPDX-License-Identifier: GPL-2.0 OR BSD-2-Clause

#include <linux/errno.h>
#include <linux/init.h>
#include <linux/ktime.h>
#include <linux/list.h>
#include <linux/module.h>
#include <linux/moduleparam.h>
#include <linux/printk.h>
#include <linux/slab.h>

struct hello_event {
	struct list_head list;
	ktime_t timestamp;
};

static unsigned int count = 1;
module_param(count, uint, 0444);
MODULE_PARM_DESC(count, "Number of times to print Hello, world!");

static LIST_HEAD(event_list);

static void free_events(bool print_timestamps)
{
	struct hello_event *event;
	struct hello_event *next;

	list_for_each_entry_safe(event, next, &event_list, list) {
		if (print_timestamps)
			pr_info("event time: %lld ns\n",
				(long long)ktime_to_ns(event->timestamp));

		list_del(&event->list);
		kfree(event);
	}
}

static int __init hello_init(void)
{
	struct hello_event *event;
	unsigned int i;

	if (count > 10) {
		pr_err("count=%u is greater than 10\n", count);
		return -EINVAL;
	}

	if (count == 0 || (count >= 5 && count <= 10))
		pr_warn("count=%u is unusual; continuing\n", count);

	for (i = 0; i < count; i++) {
		event = kmalloc(sizeof(*event), GFP_KERNEL);
		if (!event) {
			free_events(false);
			return -ENOMEM;
		}

		event->timestamp = ktime_get();
		list_add_tail(&event->list, &event_list);
		pr_info("Hello, world!\n");
	}

	return 0;
}

static void __exit hello_exit(void)
{
	free_events(true);
}

module_init(hello_init);
module_exit(hello_exit);

MODULE_AUTHOR("Artem Davydchuk");
MODULE_DESCRIPTION("Hello module with parameters, timestamps and a kernel list");
MODULE_LICENSE("Dual BSD/GPL");
