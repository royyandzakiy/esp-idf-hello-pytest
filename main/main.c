// hello_world/main/hello_world.c

#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "driver/gpio.h"
#include "esp_chip_info.h"

#define BLINK_GPIO 2 // Built-in LED on most ESP32 dev boards

static const char *TAG = "HELLO_WORLD";

// Function to blink LED
void blink_led(int times, int delay_ms) {
	gpio_set_direction(BLINK_GPIO, GPIO_MODE_OUTPUT);

	for (int i = 0; i < times; i++) {
		gpio_set_level(BLINK_GPIO, 1);
		vTaskDelay(delay_ms / portTICK_PERIOD_MS);
		gpio_set_level(BLINK_GPIO, 0);
		vTaskDelay(delay_ms / portTICK_PERIOD_MS);
	}
}

void generate_test_pattern() {
	// Generate a predictable pattern for testing
	for (int i = 0; i < 10; i++) {
		printf("TEST_PATTERN:%d:%d\n", i, i * 100);
	}
}

// Function to print system info
void print_system_info() {
	esp_chip_info_t chip_info;
	esp_chip_info(&chip_info);

	printf("Chip Info:\n");
	printf("  Model: %s\n", CONFIG_IDF_TARGET);
	printf("  Cores: %d\n", chip_info.cores);
	printf("  Revision: %d\n", chip_info.revision);
	printf("  Free Heap: %d bytes\n", esp_get_free_heap_size());
	printf("  Minimum Free Heap: %d bytes\n", esp_get_minimum_free_heap_size());
}

// Test function for various operations
void run_tests() {
	ESP_LOGI(TAG, "Running tests...");

	// Memory test
	void *test_mem = malloc(1024);
	if (test_mem) {
		ESP_LOGI(TAG, "Memory allocation test passed");
		free(test_mem);
	} else {
		ESP_LOGE(TAG, "Memory allocation test failed");
	}

	// GPIO test
	blink_led(3, 200);
	ESP_LOGI(TAG, "GPIO test completed");
}

void app_main() {
	// Initialize NVS
	esp_err_t ret = nvs_flash_init();
	if (ret == ESP_ERR_NVS_NO_FREE_PAGES ||
	    ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
		ESP_ERROR_CHECK(nvs_flash_erase());
		ret = nvs_flash_init();
	}
	ESP_ERROR_CHECK(ret);

	printf("\n=== ESP32 Hello World Application ===\n");

	// Print system information
	print_system_info();

	generate_test_pattern();

	// Run tests
	run_tests();

	// Main application loop
	int counter = 0;
	while (counter < 5) {
		printf("Hello World! Counter: %d\n", counter);
		ESP_LOGI(TAG, "Log message - Counter: %d", counter);

		blink_led(1, 100);

		counter++;
		vTaskDelay(100 / portTICK_PERIOD_MS);
	}

	printf("Restarting now.\n");
	fflush(stdout);

	// Clean blink before restart
	blink_led(1, 50);

	vTaskDelay(2000 / portTICK_PERIOD_MS);
	esp_restart();
}