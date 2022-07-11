/**
 * @file   P1F2.c
 * @author Roger Marcen
 * @date   2021/2022
*/

#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/gpio.h>                 // Required for the GPIO functions
#include <linux/interrupt.h>            // Required for the IRQ code

static unsigned int gpioButtonPlay = 27;    //GPIO27 per Play
static unsigned int gpioButtonPause = 22;     //GPIO22 per Pause
static unsigned int gpioButtonSeguent = 5;    //GPIO5 per Seguent
static unsigned int gpioButtonAnterior = 6;   //GPIO6 per Anterior
static unsigned int irqNumberPlay;
static unsigned int irqNumberPause;
static unsigned int irqNumberSeguent;
static unsigned int irqNumberAnterior;

static irq_handler_t  play(unsigned int irq, void *dev_id, struct pt_regs *regs);
static irq_handler_t  pause(unsigned int irq, void *dev_id, struct pt_regs *regs);
static irq_handler_t  seguent(unsigned int irq, void *dev_id, struct pt_regs *regs);
static irq_handler_t  anterior(unsigned int irq, void *dev_id, struct pt_regs *regs);


static irq_handler_t play(unsigned int irq, void *dev_id, struct pt_regs *regs){

   return (irq_handler_t) IRQ_HANDLED;
}

static irq_handler_t pause(unsigned int irq, void *dev_id, struct pt_regs *regs){

   return (irq_handler_t) IRQ_HANDLED;
}

static irq_handler_t seguent(unsigned int irq, void *dev_id, struct pt_regs *regs){

   return (irq_handler_t) IRQ_HANDLED;
}

static irq_handler_t anterior(unsigned int irq, void *dev_id, struct pt_regs *regs){

   return (irq_handler_t) IRQ_HANDLED;
}

static int __init my_init(void){
    int result = 0;
    printk(KERN_INFO "Inicialitzant Musica LKM\n");

    // Iniciem boto Play
    gpio_request(gpioButtonPlay, "sysfs");       
    gpio_direction_input(gpioButtonPlay);       
    gpio_set_debounce(gpioButtonPlay, 200);      
    gpio_export(gpioButtonPlay, false);

    // Iniciem boto Pause
    gpio_request(gpioButtonPause, "sysfs");       
    gpio_direction_input(gpioButtonPause);       
    gpio_set_debounce(gpioButtonPause, 200);      
    gpio_export(gpioButtonPause, false);

    // Iniciem boto Seguent
    gpio_request(gpioButtonSeguent, "sysfs");       
    gpio_direction_input(gpioButtonSeguent);       
    gpio_set_debounce(gpioButtonSeguent, 200);      
    gpio_export(gpioButtonSeguent, false); 

    // Iniciem boto Anterior
    gpio_request(gpioButtonOffAnterior, "sysfs");       
    gpio_direction_input(gpioButtonAnterior);       
    gpio_set_debounce(gpioButtonAnterior, 200);      
    gpio_export(gpioButtonAnterior, false);
                                
    // Relacionem les interrupcions amb els botons
    irqNumberPlay = gpio_to_irq(gpioButtonPlay);
    irqNumberPause = gpio_to_irq(gpioButtonPause);
    irqNumberSeguent = gpio_to_irq(gpioButtonSeguent);
    irqNumberAnterior = gpio_to_irq(gpioButtonAnterior);

    // This next call requests an interrupt line
    result = request_irq(irqNumberPlay, (irq_handler_t) play, IRQF_TRIGGER_RISING, "Play", NULL);                 
    result = request_irq(irqNumberPause, (irq_handler_t) pause, IRQF_TRIGGER_RISING, "Pause", NULL);
    result = request_irq(irqNumberSeguent, (irq_handler_t) seguent, IRQF_TRIGGER_RISING, "Seguent", NULL);                 
    result = request_irq(irqNumberAnterior, (irq_handler_t) anterior, IRQF_TRIGGER_RISING, "Anterior", NULL);                 

    return result;
}

static void __exit my_exit(void){
   free_irq(irqNumberPlay, NULL);
   free_irq(irqNumberPause, NULL);
   free_irq(irqNumberSeguent, NULL);
   free_irq(irqNumberAnterior, NULL);               
   gpio_unexport(gpioButtonPlay);
   gpio_unexport(gpioButtonPause);
   gpio_unexport(gpioButtonSeguent);
   gpio_unexport(gpioButtonAnterior);
   gpio_free(gpioButtonPlay);
   gpio_free(gpioButtonPause);
   gpio_free(gpioButtonSeguent);
   gpio_free(gpioButtonAnterior); 
   return;                  
}

module_init(my_init);
module_exit(my_exit);
MODULE_LICENSE("GPL");
