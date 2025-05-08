#include "pico/cyw43_arch.h"
#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/adc.h"
#include "pico/async_context.h"
#include "lwip/altcp_tls.h"
#include "example_http_client_util.h"

#define HOST "192.168.31.116"
#define PORT 5000

const char* get_direction(uint adc_x_raw, uint adc_y_raw) {
    #define ADC_MAX ((1 << 12) - 1)
    if (adc_y_raw < ADC_MAX / 4 && adc_x_raw < ADC_MAX / 4) {
        return "Sudoeste";
    } else if (adc_y_raw < ADC_MAX / 4 && adc_x_raw > 3 * ADC_MAX / 4) {
        return "Sudeste";
    } else if (adc_y_raw > 3 * ADC_MAX / 4 && adc_x_raw < ADC_MAX / 4) {
        return "Noroeste";
    } else if (adc_y_raw > 3 * ADC_MAX / 4 && adc_x_raw > 3 * ADC_MAX / 4) {
        return "Nordeste";
    } else if (adc_y_raw < ADC_MAX / 3) {
        return "Sul";
    } else if (adc_y_raw > 2 * ADC_MAX / 3) {
        return "Norte";
    } else if (adc_x_raw < ADC_MAX / 3) {
        return "Oeste";
    } else if (adc_x_raw > 2 * ADC_MAX / 3) {
        return "Leste";
    } else {
        return "Centro";
    }
}

void send_direction_data(uint adc_x, uint adc_y) {
    char url[128];
    snprintf(url, sizeof(url), "/data?x=%u&y=%u", adc_x, adc_y);

    EXAMPLE_HTTP_REQUEST_T req = {0};
    req.hostname   = HOST;
    req.url        = url;
    req.port       = PORT;
    req.headers_fn = http_client_header_print_fn;
    req.recv_fn    = http_client_receive_print_fn;

    printf("Enviando requisição HTTP para %s:%d%s\n", HOST, PORT, url);
    http_client_request_sync(cyw43_arch_async_context(), &req);
}

int main() {
    stdio_init_all();
    adc_init();

    if (cyw43_arch_init()) {
        printf("Erro ao inicializar o Wi-Fi\n");
        return 1;
    }

    cyw43_arch_enable_sta_mode();
    printf("Conectando ao Wi-Fi \"%s\"…\n", WIFI_SSID);

    if (cyw43_arch_wifi_connect_timeout_ms(WIFI_SSID, WIFI_PASSWORD,
                                           CYW43_AUTH_WPA2_AES_PSK, 10000)) {
        printf("Falha ao conectar ao Wi-Fi\n");
        return 1;
    }
    printf("Wi-Fi conectado!\n");
    uint8_t *ip = (uint8_t*)&(cyw43_state.netif[0].ip_addr.addr);
    printf("Endereço IP %d.%d.%d.%d\n", ip[0], ip[1], ip[2], ip[3]);

    while (true) {
        adc_select_input(0);
        uint adc_y_raw = adc_read();
        adc_select_input(1);
        uint adc_x_raw = adc_read();

        const char* direction = get_direction(adc_x_raw, adc_y_raw);
        printf("X: %u, Y: %u, Direção: %s\n", adc_x_raw, adc_y_raw, direction);

        send_direction_data(adc_x_raw, adc_y_raw);
        sleep_ms(500);
    }

    cyw43_arch_deinit();
    return 0;
}
