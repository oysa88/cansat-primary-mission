function samle_data () {
    tid = input.runningTime()
    teller += 1
    analog_NTC = pins.analogReadPin(AnalogReadWritePin.P10)
    spenning_NTC = avrund(analog_NTC / 1024 * Uref, 3)
    trykk = BME280.pressure(BME280_P.Pa)
    temp_NTC = avrund(39.8 * spenning_NTC - 42.76, 2)
}
function avrund (verdi: number, desimaler: number) {
    faktor = 10 ** desimaler
    return Math.round(verdi * faktor) / faktor
}
function lagre_data () {
    datalogger.log(
    datalogger.createCV("Callsign", callsign),
    datalogger.createCV("Tid (ms)", tid),
    datalogger.createCV("Teller", teller),
    datalogger.createCV("Trykk", trykk),
    datalogger.createCV("Temperatur", temp_NTC)
    )
}
function sende_data () {
    pxtlora.e32SendString("" + callsign + ";" + ("" + tid) + ";" + ("" + teller) + ";" + ("" + trykk) + ";" + ("" + temp_NTC))
}
function skrive_data () {
    kitronik_VIEW128x64.clear()
    kitronik_VIEW128x64.show("Analog NTC: " + analog_NTC, 1)
    kitronik_VIEW128x64.show("Spenning NTC: " + spenning_NTC + " V", 2)
    kitronik_VIEW128x64.show("Temp. NTC: " + temp_NTC + " C", 3)
    kitronik_VIEW128x64.show("Trykk: " + trykk + " Pa", 4)
}
let faktor = 0
let temp_NTC = 0
let trykk = 0
let spenning_NTC = 0
let analog_NTC = 0
let teller = 0
let tid = 0
let Uref = 0
let callsign = ""
pxtlora.e32Init(
DigitalPin.P8,
DigitalPin.P9,
DigitalPin.P16,
SerialPin.P14,
SerialPin.P15,
BaudRate.BaudRate9600,
false
)
callsign = "TLNT"
Uref = 3
kitronik_VIEW128x64.controlDisplayOnOff(kitronik_VIEW128x64.onOff(true))
kitronik_VIEW128x64.setFontSize(kitronik_VIEW128x64.FontSelection.Normal)
BME280.PowerOn()
BME280.Address(BME280_I2C_ADDRESS.ADDR_0x76)
basic.forever(function () {
    samle_data()
    skrive_data()
    lagre_data()
    sende_data()
    basic.pause(500)
})
