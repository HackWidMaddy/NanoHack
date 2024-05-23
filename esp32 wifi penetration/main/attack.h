
#ifndef ATTACK_H
#define ATTACK_H

#include "esp_wifi_types.h"


typedef enum {
    ATTACK_TYPE_PASSIVE,
    ATTACK_TYPE_HANDSHAKE,
    ATTACK_TYPE_PMKID,
    ATTACK_TYPE_DOS
} attack_type_t;

/**
 * @brief States of single attack run. 
 * 
 * @note TIMEOUT will be removed in #64
 */
typedef enum {
    READY,      ///< no attack is in progress and results from previous attack run are available.
    RUNNING,    ///< attack is in progress, attack_status_t.content may not be consistent.
    FINISHED,   ///< last attack finsihed and results are available.
    TIMEOUT     ///< last attack timed out. This option will be moved as sub category of FINISHED state.
} attack_state_t;


typedef struct {
    uint8_t type;
    uint8_t method;
    uint8_t timeout;
    const wifi_ap_record_t *ap_record;
} attack_config_t;

/**
 * @brief Contains current attack status.
 * 
 * This structure contains all information and data about latest attack.
 */
typedef struct {
    uint8_t state;  ///< attack_state_t
    uint8_t type;   ///< attack_type_t
    uint16_t content_size;
    char *content;
} attack_status_t;


const attack_status_t *attack_get_status();

void attack_update_status(attack_state_t state);


void attack_init();


char *attack_alloc_result_content(unsigned size);


void attack_append_status_content(uint8_t *buffer, unsigned size);

#endif