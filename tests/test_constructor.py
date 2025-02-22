"""
Constructor method tests for pyubx2.UBXMessage

Created on 21 Oct 2020

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""
# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import unittest

from pyubx2 import UBXMessage, UBXReader, GET, SET, POLL


class FillTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def testFill_CFGMSG(self):  # test POLL constructor fill, format 1
        EXPECTED_RESULT = "<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=VTG)>"
        res = UBXMessage("CFG", "CFG-MSG", POLL, msgClass=240, msgID=5)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGMSG2(self):  # test POLL constructor fill, format 2
        EXPECTED_RESULT = "<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=VTG)>"
        res = UBXMessage(b"\x06", b"\x01", POLL, msgClass=240, msgID=5)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGMSG3(self):  # test POLL constructor fill, format 3
        EXPECTED_RESULT = "<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=VTG)>"
        res = UBXMessage(6, 1, POLL, msgClass=240, msgID=5)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGMSG4(self):  # test SET constructor fill
        EXPECTED_RESULT = "<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=GLL, rateDDC=0, rateUART1=1, rateUART2=0, rateUSB=1, rateSPI=0, reserved=0)>"
        res = UBXMessage(
            "CFG", "CFG-MSG", SET, msgClass=240, msgID=1, rateUART1=1, rateUSB=1
        )
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_INFNOTICE(
        self,
    ):  # test INF-NOTICE variable length message constructor fill
        EXPECTED_RESULT = "<UBX(INF-NOTICE, message=Lorem ipsum dolor sit amet)>"
        res = UBXMessage("INF", "INF-NOTICE", GET, message="Lorem ipsum dolor sit amet")
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGNMEA(self):  # test SET constructor fill, set all values
        EXPECTED_RESULT = "<UBX(CFG-NMEA, posFilt=0, mskPosFilt=0, timeFilt=0, dateFilt=0, gpsOnlyFilter=0, trackFilt=0, nmeaVersion=64, numSV=4, compat=0, consider=0, limit82=0, highPrec=0, disableGps=0, disableSbas=0, disableGalileo=0, disableQzss=0, disableGlonass=0, disableBeidou=0, svNumbering=0, mainTalkerId=0, gsvTalkerId=0, version=0, bdsTalkerId=b'\\x00\\x00', reserved1=0)>"
        res = UBXMessage(
            "CFG",
            "CFG-NMEA",
            SET,
            filter=b"\x45",
            nmeaVersion=64,
            numSV=4,
            flags=b"\x14",
        )
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGNMEA2(
        self,
    ):  # test SET constructor fill, set some values, default others
        EXPECTED_RESULT = "<UBX(CFG-NMEA, posFilt=0, mskPosFilt=0, timeFilt=0, dateFilt=0, gpsOnlyFilter=0, trackFilt=0, nmeaVersion=35, numSV=1, compat=0, consider=0, limit82=0, highPrec=0, disableGps=0, disableSbas=0, disableGalileo=0, disableQzss=0, disableGlonass=0, disableBeidou=0, svNumbering=0, mainTalkerId=0, gsvTalkerId=0, version=0, bdsTalkerId=b'\\x00\\x00', reserved1=0)>"
        res = UBXMessage("CFG", "CFG-NMEA", SET, nmeaVersion=35, numSV=1)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGNMEAPARSE(
        self,
    ):  # check that raw payload is correctly populated and parses back to original message
        EXPECTED_RESULT = "<UBX(CFG-NMEA, posFilt=0, mskPosFilt=0, timeFilt=0, dateFilt=0, gpsOnlyFilter=0, trackFilt=0, nmeaVersion=35, numSV=1, compat=0, consider=0, limit82=0, highPrec=0, disableGps=0, disableSbas=0, disableGalileo=0, disableQzss=0, disableGlonass=0, disableBeidou=0, svNumbering=0, mainTalkerId=0, gsvTalkerId=0, version=0, bdsTalkerId=b'\\x00\\x00', reserved1=0)>"
        res = UBXMessage("CFG", "CFG-NMEA", SET, nmeaVersion=35, numSV=1)
        res2 = UBXReader.parse(res.serialize())
        self.assertEqual(str(res2), EXPECTED_RESULT)

    def testFill_CFGNMEAPOLL(self):  # test POLL constructor, no payload
        EXPECTED_RESULT = "<UBX(CFG-NMEA)>"
        res = UBXMessage("CFG", "CFG-NMEA", POLL)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGNMEAPOLL2(self):  # test POLL constructor, no payload
        EXPECTED_RESULT = "<UBX(CFG-NMEA)>"
        res = UBXMessage("CFG", "CFG-NMEA", POLL)
        res2 = UBXReader.parse(res.serialize())
        self.assertEqual(str(res2), EXPECTED_RESULT)

    def testFill_CFGGNSS(self):  #  test CFG-GNSS SET multiple repeats in group
        EXPECTED_RESULT = "<UBX(CFG-GNSS, msgVer=0, numTrkChHw=2, numTrkChUse=4, numConfigBlocks=2, gnssId_01=GPS, resTrkCh_01=4, maxTrkCh_01=32, reserved0_01=0, enable_01=1, sigCfMask_01=4, gnssId_02=GLONASS, resTrkCh_02=3, maxTrkCh_02=24, reserved0_02=0, enable_02=0, sigCfMask_02=64)>"
        res = UBXMessage(
            "CFG",
            "CFG-GNSS",
            SET,
            numTrkChHw=2,
            numTrkChUse=4,
            numConfigBlocks=2,
            gnssId_01=0,
            resTrkCh_01=4,
            maxTrkCh_01=32,
            enable_01=1,
            sigCfMask_01=4,
            gnssId_02=6,
            resTrkCh_02=3,
            maxTrkCh_02=24,
            enable_02=0,
            sigCfMask_02=64,
        )
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGGNSS_NOBITFIELD(
        self,
    ):  #  test CFG-GNSS SET with parsebitfield = False
        EXPECTED_RESULT = "<UBX(CFG-GNSS, msgVer=0, numTrkChHw=2, numTrkChUse=4, numConfigBlocks=2, gnssId_01=GPS, resTrkCh_01=4, maxTrkCh_01=32, reserved0_01=0, flags_01=b'\\x01\\x00\\x04\\x00', gnssId_02=GLONASS, resTrkCh_02=3, maxTrkCh_02=24, reserved0_02=0, flags_02=b'\\x00\\x00@\\x00')>"
        EXPECTED_RESULT2 = "<UBX(CFG-GNSS, msgVer=0, numTrkChHw=2, numTrkChUse=4, numConfigBlocks=2, gnssId_01=GPS, resTrkCh_01=4, maxTrkCh_01=32, reserved0_01=0, enable_01=1, sigCfMask_01=4, gnssId_02=GLONASS, resTrkCh_02=3, maxTrkCh_02=24, reserved0_02=0, enable_02=0, sigCfMask_02=64)>"
        res = UBXMessage(
            "CFG",
            "CFG-GNSS",
            SET,
            parsebitfield=False,
            numTrkChHw=2,
            numTrkChUse=4,
            numConfigBlocks=2,
            gnssId_01=0,
            resTrkCh_01=4,
            maxTrkCh_01=32,
            flags_01=b"\x01\x00\x04\x00",
            gnssId_02=6,
            resTrkCh_02=3,
            maxTrkCh_02=24,
            flags_02=b"\x00\x00\x40\x00",
        )
        self.assertEqual(str(res), EXPECTED_RESULT)
        res2 = UBXReader.parse(
            res.serialize()
        )  # reconstruct message and parse again with parsebitfield = True
        self.assertEqual(str(res2), EXPECTED_RESULT2)

    def testFill_CFGDOSC(self):  # test CFG-DOSC multiple repeats in group
        EXPECTED_RESULT = "<UBX(CFG-DOSC, version=23, numOsc=2, reserved1=0, oscId_01=4, reserved2_01=0, isCalibrated_01=0, controlIf_01=0, freq_01=22, phaseOffset_01=0, withTemp_01=0, withAge_01=0, timeToTemp_01=0, reserved3_01=0, gainVco_01=0, gainUncertainty_01=0, reserved4_01=0, oscId_02=7, reserved2_02=0, isCalibrated_02=0, controlIf_02=0, freq_02=44, phaseOffset_02=0, withTemp_02=0, withAge_02=0, timeToTemp_02=0, reserved3_02=0, gainVco_02=0, gainUncertainty_02=0, reserved4_02=0)>"
        res = UBXMessage(
            "CFG",
            "CFG-DOSC",
            SET,
            version=23,
            numOsc=2,
            oscId_01=4,
            freq_01=22,
            oscId_02=7,
            freq_02=44,
        )
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGDOSC1(self):  # test CFG-DOSC single repeat in group
        EXPECTED_RESULT = "<UBX(CFG-DOSC, version=37, numOsc=1, reserved1=0, oscId_01=8, reserved2_01=0, isCalibrated_01=0, controlIf_01=0, freq_01=53, phaseOffset_01=26, withTemp_01=0, withAge_01=0, timeToTemp_01=0, reserved3_01=0, gainVco_01=4, gainUncertainty_01=123, reserved4_01=0)>"
        res = UBXMessage(
            "CFG",
            "CFG-DOSC",
            SET,
            version=37,
            numOsc=1,
            oscId_01=8,
            freq_01=53,
            phaseOffset_01=26,
            gainVco_01=4,
            gainUncertainty_01=123,
        )
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGDOSCPARSE(
        self,
    ):  # test CFG-DOSC check that raw payload is correctly populated and parses back to original message
        EXPECTED_RESULT = "<UBX(CFG-DOSC, version=37, numOsc=1, reserved1=0, oscId_01=8, reserved2_01=0, isCalibrated_01=0, controlIf_01=0, freq_01=53, phaseOffset_01=26, withTemp_01=0, withAge_01=0, timeToTemp_01=0, reserved3_01=0, gainVco_01=4, gainUncertainty_01=123, reserved4_01=0)>"
        res = UBXMessage(
            "CFG",
            "CFG-DOSC",
            SET,
            version=37,
            numOsc=1,
            oscId_01=8,
            freq_01=53,
            phaseOffset_01=26,
            gainVco_01=4,
            gainUncertainty_01=123,
        )
        res2 = UBXReader.parse(res.serialize())
        self.assertEqual(str(res2), EXPECTED_RESULT)

    def testFill_CFGDOSC2(self):  # test CFG-DOSC empty group
        EXPECTED_RESULT = "<UBX(CFG-DOSC, version=37, numOsc=0, reserved1=0)>"
        res = UBXMessage("CFG", "CFG-DOSC", SET, version=37, numOsc=0)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGDAT(
        self,
    ):  # test CFG-DAT floating point attribute, single and double precision
        EXPECTED_RESULT = "<UBX(CFG-DAT, datumNum=0, datumName=b'\\x00\\x00\\x00\\x00\\x00\\x00', majA=4321.123456789128, flat=-2964.00469836, dX=-1.2345678, dY=27.40654, dZ=0.0, rotX=0.0, rotY=0.0, rotZ=0.0, scale=0.0)>"
        res = UBXMessage(
            "CFG",
            "CFG-DAT",
            SET,
            majA=4321.123456789128,
            flat=-2964.00469836,
            dX=-1.2345678,
            dY=27.40654,
        )
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGDATPARSE(
        self,
    ):  # check that raw payload is correctly populated and parses back to original message
        EXPECTED_RESULT = "<UBX(CFG-DAT, datumNum=0, datumName=b'\\x00\\x00\\x00\\x00\\x00\\x00', majA=4321.123456789128, flat=-2964.00469836, dX=-1.2345677614212036, dY=27.406539916992188, dZ=0.0, rotX=0.0, rotY=0.0, rotZ=0.0, scale=0.0)>"
        res = UBXMessage(
            "CFG",
            "CFG-DAT",
            SET,
            majA=4321.123456789128,
            flat=-2964.00469836,
            dX=-1.2345678,
            dY=27.40654,
        )
        res2 = UBXReader.parse(res.serialize(), msgmode=SET)
        self.assertEqual(str(res2), EXPECTED_RESULT)

    def testFill_CFGDATPARSE2(
        self,
    ):  # check that raw payload is correctly populated and parses back to original message
        EXPECTED_RESULT = "<UBX(CFG-DAT, datumNum=0, datumName=b'\\x00\\x00\\x00\\x00\\x00\\x00', majA=0.0, flat=0.0, dX=-1.2345677614212036, dY=27.406539916992188, dZ=0.0, rotX=0.0, rotY=0.0, rotZ=0.0, scale=0.0)>"
        res = UBXMessage(
            "CFG",
            "CFG-DAT",
            SET,
            dX=-1.2345678,
            dY=27.40654,
        )
        res2 = UBXReader.parse(res.serialize(), msgmode=SET)
        self.assertEqual(str(res2), EXPECTED_RESULT)

    def testEVAL(
        self,
    ):  # double check that eval of repr(msg) reproduces original message
        res1 = UBXMessage("CFG", "CFG-MSG", POLL, msgClass=240, msgID=5)
        res2 = eval(repr(res1))
        self.assertEqual(str(res1), str(res2))

    def testEVAL2(
        self,
    ):  # double check that eval of repr(msg) reproduces original message
        res1 = UBXMessage(
            "CFG", "CFG-MSG", SET, msgClass=240, msgID=5, rateUART1=1, rateUSB=1
        )
        res2 = eval(repr(res1))
        self.assertEqual(str(res1), str(res2))

    def testFill_NAVSBAS(self):  #  test NAV-SBAS GET constructor with bit flags
        EXPECTED_RESULT = "<UBX(NAV-SBAS, iTOW=23:59:44, geo=1, mode=0, sys=0, Ranging=1, Corrections=0, Integrity=1, Testmode=0, Bad=1, numCh=0, integrityUsed=1, reserved0=0)>"
        res = UBXMessage(
            "NAV",
            "NAV-SBAS",
            GET,
            geo=1,
            mode=0,
            sys=0,
            Ranging=1,
            Corrections=0,
            Integrity=1,
            Testmode=0,
            Bad=1,
            numCh=0,
            integrityUsed=1,
        )
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testEval_NAVBAS(self):  # test payload is correctly set for bit flags
        res1 = UBXMessage(
            "NAV",
            "NAV-SBAS",
            GET,
            geo=1,
            mode=0,
            sys=0,
            Ranging=1,
            Corrections=0,
            Integrity=1,
            Testmode=0,
            Bad=1,
            numCh=0,
            integrityUsed=1,
        )
        res2 = UBXMessage("NAV", "NAV-SBAS", GET, payload=res1.payload)
        self.assertEqual(str(res1), str(res2))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
