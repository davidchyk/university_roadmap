// SPDX-License-Identifier: GPL-2.0 OR BSD-2-Clause

#include <linux/init.h>
#include <linux/ktime.h>
#include <linux/list.h>
#include <linux/module.h>
#include <linux/printk.h>
#include <linux/slab.h>

#include "hello1.h"

struct hello_event {
	struct list_head list;
	ktime_t start;
	ktime_t finish;
};

static LIST_HEAD(event_list);

int print_hello(void)
{
	struct hello_event *event;

	event = kmalloc(sizeof(*event), GFP_KERNEL);
	if (!event)
		return -ENOMEM;

	event->start = ktime_get();
	pr_info("Hello, world!\n");
	event->finish = ktime_get();
	list_add_tail(&event->list, &event_list);

	return 0;
}
EXPORT_SYMBOL(print_hello);

static int __init hello1_init(void)
{
	pr_info("hello1 loaded\n");
	return 0;
}

static void __exit hello1_exit(void)
{
	struct hello_event *event;
	struct hello_event *next;

	list_for_each_entry_safe(event, next, &event_list, list) {
		pr_info("print duration: %lld ns\n",
			(long long)ktime_to_ns(ktime_sub(event->finish,
							 event->start)));
		list_del(&event->list);
		kfree(event);
	}

	pr_info("hello1 unloaded\n");
}

module_init(hello1_init);
module_exit(hello1_exit);

MODULE_AUTHOR("Artem Davydchuk");
MODULE_DESCRIPTION("Hello service with timing and a kernel list");
MODULE_LICENSE("Dual BSD/GPL");
