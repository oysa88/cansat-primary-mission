def samle_data():
    global analog_NTC, analog_TMP36, spenning_NTC, spenning_TMP36, trykk, temp_BME280, temp_TMP36, temp_NTC, teller, tid
    analog_NTC = pins.analog_read_pin(AnalogReadWritePin.P10)
    analog_TMP36 = pins.analog_read_pin(AnalogReadWritePin.P0)
    spenning_NTC = Math.round(analog_NTC / 1024 * Uref * 1000) / 1000
    spenning_TMP36 = Math.round(analog_TMP36 / 1024 * Uref * 1000) / 1000
    trykk = BME280.pressure(BME280_P.PA)
    temp_BME280 = BME280.temperature(BME280_T.T_C)
    temp_TMP36 = (spenning_TMP36 - 0.5) / 0.01 - 0
    temp_NTC = Math.round((39.8 * spenning_NTC - 42.76) * 10) / 10
    teller += 1
    tid = input.running_time()
def lagre_data():
    datalogger.log(datalogger.create_cv("Callsign", callsign),
        datalogger.create_cv("Tid (ms)", tid),
        datalogger.create_cv("Teller", teller),
        datalogger.create_cv("Trykk", trykk),
        datalogger.create_cv("Temperatur", temp_BME280))
def sende_data():
    pxtlora.e32_send_string("" + callsign + ";" + ("" + str(tid)) + ";" + ("" + str(teller)) + ";" + ("" + str(trykk)) + ";" + ("" + str(temp_BME280)))
def skrive_data():
    kitronik_VIEW128x64.clear()
    kitronik_VIEW128x64.show("Analog NTC: " + ("" + str(analog_NTC)), 1)
    kitronik_VIEW128x64.show("Analog TMP36: " + ("" + str(analog_TMP36)), 2)
    kitronik_VIEW128x64.show("Spenning NTC: " + ("" + str(spenning_NTC)) + " V", 3)
    kitronik_VIEW128x64.show("Spenning TMP36: " + ("" + str(spenning_TMP36)) + " V", 4)
    kitronik_VIEW128x64.show("Temp. BME28: " + ("" + str(temp_BME280)) + " C", 5)
    kitronik_VIEW128x64.show("Temp. TMP36: " + ("" + str(temp_TMP36)) + " C", 6)
    kitronik_VIEW128x64.show("Temp. NTC: " + ("" + str(temp_NTC)) + " C", 7)
tid = 0
teller = 0
temp_NTC = 0
temp_TMP36 = 0
temp_BME280 = 0
trykk = 0
spenning_TMP36 = 0
spenning_NTC = 0
analog_TMP36 = 0
analog_NTC = 0
Uref = 0
callsign = ""
pxtlora.e32_init(DigitalPin.P8,
    DigitalPin.P9,
    DigitalPin.P16,
    SerialPin.P14,
    SerialPin.P15,
    BaudRate.BAUD_RATE9600,
    False)
callsign = "TLNT"
Uref = 3
kitronik_VIEW128x64.control_display_on_off(kitronik_VIEW128x64.on_off(True))
kitronik_VIEW128x64.set_font_size(kitronik_VIEW128x64.FontSelection.NORMAL)
BME280.power_on()
BME280.address(BME280_I2C_ADDRESS.ADDR_0X76)

def on_forever():
    samle_data()
    skrive_data()
    lagre_data()
    sende_data()
    basic.pause(500)
basic.forever(on_forever)
