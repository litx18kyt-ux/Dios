import React, { useState } from 'react';
import { Calendar, Search, Save, Download, Check, Plus, Trash2, Eye, EyeOff, Sparkles, Filter } from 'lucide-react';
import { memoryStore } from '../../data/memoryStore';

interface MslDoctor {
  srNo: number;
  doctorName: string;
  activityType: string;
  speciality: string;
  dob: string;
  doa: string;
  apr: string;
  may: string;
  jun: string;
  jul: string;
  aug: string;
  sept: string;
  oct: string;
  nov: string;
  dec: string;
  jan: string;
  feb: string;
  mar: string;
}

const FULL_123_MSL_DOCTORS: MslDoctor[] = [
  {
    "srNo": 23,
    "doctorName": "Abhay jain",
    "activityType": "CRM",
    "speciality": "CONSULTANT PHYSICIAN",
    "dob": "12/12/1972",
    "doa": "",
    "apr": "1,7,10,17,21,24,27,29",
    "may": "6,8,11,19,26,27,29",
    "jun": "1,2,12,16,18,",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 50,
    "doctorName": "ABHIJEET BASU",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "12/12/1972",
    "doa": "",
    "apr": "7,9,11,17,24",
    "may": "4,6,8,15,18",
    "jun": "13,19,29",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 61,
    "doctorName": "Abhishek Kumar",
    "activityType": "",
    "speciality": "CONSPHYS",
    "dob": "",
    "doa": "",
    "apr": "2,10,17,23,24,28,30",
    "may": "15,21,28",
    "jun": "12,18,25",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 10,
    "doctorName": "AKVATS",
    "activityType": "CRM",
    "speciality": "DM NEURO",
    "dob": "02/08/2019",
    "doa": "",
    "apr": "1,15,23,30",
    "may": "6,14,21",
    "jun": "3,18,24",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 59,
    "doctorName": "Ameet Mehta",
    "activityType": "",
    "speciality": "GENERAL PHYSICIAN",
    "dob": "27/04/1900",
    "doa": "19/05/1900",
    "apr": "3,13,17,24,27",
    "may": "8,15,28,29",
    "jun": "1,3,16",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 37,
    "doctorName": "AMIT KHANDELWAL",
    "activityType": "WCFYH VAL/VIN",
    "speciality": "CARDIO",
    "dob": "03/04/1977",
    "doa": "",
    "apr": "out of Town ,21",
    "may": "",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 66,
    "doctorName": "ANIS JUKARWALA",
    "activityType": "",
    "speciality": "MD",
    "dob": "",
    "doa": "",
    "apr": "1,10,30",
    "may": "18,27",
    "jun": "12,out of town",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 20,
    "doctorName": "ANISH JAIN",
    "activityType": "CRM",
    "speciality": "MD MED",
    "dob": "16/12/2019",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "11,na",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 86,
    "doctorName": "ANMOL PAGARIYA",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "23/01/2019",
    "doa": "",
    "apr": "6,22",
    "may": "7,22",
    "jun": "4,23",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 96,
    "doctorName": "ANUBHAV BANSAL",
    "activityType": "",
    "speciality": "CVTS",
    "dob": "",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 74,
    "doctorName": "ANURAG JAIN",
    "activityType": "",
    "speciality": "DNB NEFRO",
    "dob": "12/03/1979",
    "doa": "",
    "apr": "na",
    "may": "",
    "jun": "20",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 107,
    "doctorName": "Ashutosh soni",
    "activityType": "",
    "speciality": "NEPHRO",
    "dob": "",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 114,
    "doctorName": "ASHWIN PATIDAR",
    "activityType": "",
    "speciality": "MBBS MD",
    "dob": "",
    "doa": "",
    "apr": "8",
    "may": "13,25",
    "jun": "17,26",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 22,
    "doctorName": "BALDEV MEENA",
    "activityType": "CRM",
    "speciality": "MD MED",
    "dob": "05/07/1997",
    "doa": "",
    "apr": "1,2,9,11,18,27",
    "may": "14,28,27",
    "jun": "12,22,25,29",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 57,
    "doctorName": "BHUPESH PARTANI",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "23/10/2019",
    "doa": "",
    "apr": "6,22",
    "may": "7,22",
    "jun": "4,23",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 113,
    "doctorName": "BIPIN CHANDRA ADITYA DASARI",
    "activityType": "",
    "speciality": "CARDIO",
    "dob": "13/05/1990",
    "doa": "",
    "apr": "8,16",
    "may": "ntc,",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 111,
    "doctorName": "BL KUMAWAT",
    "activityType": "",
    "speciality": "MBBB MD",
    "dob": "",
    "doa": "",
    "apr": "6,22",
    "may": "22",
    "jun": "4,23",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 6,
    "doctorName": "BS BOMB",
    "activityType": "CRM",
    "speciality": "MD MED",
    "dob": "08/12/2019",
    "doa": "",
    "apr": "4,11,15",
    "may": "8,14,18",
    "jun": "1,18",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 79,
    "doctorName": "CHIRAG RATHOR",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "03/04/1990",
    "doa": "10/02/2000",
    "apr": "25",
    "may": "2,16",
    "jun": "6,20,27",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 34,
    "doctorName": "CPPUROHIT",
    "activityType": "WCFYH VAL/VIN",
    "speciality": "DM CARDIO",
    "dob": "02/11/1971",
    "doa": "",
    "apr": "4,14,21,28",
    "may": "12,18",
    "jun": "20",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 7,
    "doctorName": "D C SHARMA",
    "activityType": "CRM",
    "speciality": "DM ENDO",
    "dob": "12/05/2019",
    "doa": "",
    "apr": "3,9,10",
    "may": "7,12,28",
    "jun": "12,18,ntc",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 108,
    "doctorName": "DEEPA KATARA",
    "activityType": "",
    "speciality": "MD PHYSICAN",
    "dob": "",
    "doa": "",
    "apr": "8,16",
    "may": "na,25",
    "jun": "na,26",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 32,
    "doctorName": "DEEPAK AAMETHA",
    "activityType": "WCFYH VAL/VIN",
    "speciality": "MD.CARDIO",
    "dob": "17/03/1980",
    "doa": "",
    "apr": "7,10,17",
    "may": "12,19,26",
    "jun": "16,19,ntc",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 120,
    "doctorName": "DEEPAK GARG",
    "activityType": "",
    "speciality": "MBBS PHY",
    "dob": "",
    "doa": "",
    "apr": "4",
    "may": "",
    "jun": "20",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 12,
    "doctorName": "DENY",
    "activityType": "CRM",
    "speciality": "DM CARDIO",
    "dob": "03/06/2019",
    "doa": "",
    "apr": "9,10,24,30(doa)",
    "may": "8,19,26,29",
    "jun": "12,18,25",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 38,
    "doctorName": "Dilip jain",
    "activityType": "WCFYH VAL/VIN",
    "speciality": "CARDIOLOGY",
    "dob": "24/04/1982",
    "doa": "",
    "apr": "4,13,17,21,27",
    "may": "18,26,29",
    "jun": "9,19,29",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 2,
    "doctorName": "DP SINGH",
    "activityType": "CRM",
    "speciality": "MD MED",
    "dob": "23/11/2019",
    "doa": "",
    "apr": "7,23,27",
    "may": "6,11,21,29,30",
    "jun": "15,24,29",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 27,
    "doctorName": "G K Mukhiya",
    "activityType": "CRM",
    "speciality": "DM NEPHRO",
    "dob": "13/05/1973",
    "doa": "",
    "apr": "3,11",
    "may": "8,15,29",
    "jun": "13,19,na",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 97,
    "doctorName": "GOURAV KUMAR MITTAL",
    "activityType": "",
    "speciality": "CARDIO",
    "dob": "11/09/1900",
    "doa": "23/06/1900",
    "apr": "27",
    "may": "",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 75,
    "doctorName": "GOVIND MANGAL",
    "activityType": "",
    "speciality": "DM NEURO",
    "dob": "",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 103,
    "doctorName": "GYANKUMAR DAKSH",
    "activityType": "",
    "speciality": "General Practitioner (GP)",
    "dob": "",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "11",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 116,
    "doctorName": "HARBEER SINGH CHHABRA",
    "activityType": "",
    "speciality": "PHY",
    "dob": "",
    "doa": "",
    "apr": "3,24",
    "may": "29",
    "jun": "12",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 92,
    "doctorName": "Harish charpota",
    "activityType": "",
    "speciality": "M B B S PHY",
    "dob": "16/10/1900",
    "doa": "27/04/1900",
    "apr": "na",
    "may": "13",
    "jun": "17,26",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 70,
    "doctorName": "HARISH SANADHY",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "01/01/1970",
    "doa": "",
    "apr": "4,14,21,28",
    "may": "12",
    "jun": "9",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 87,
    "doctorName": "HC SONI",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "25/10/1955",
    "doa": "23/11/2023",
    "apr": "6,22",
    "may": "7,22",
    "jun": "4,23",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 21,
    "doctorName": "HEMANT MAHUR",
    "activityType": "CRM",
    "speciality": "MD MED",
    "dob": "25/03/1996",
    "doa": "",
    "apr": "out of Town",
    "may": "",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 24,
    "doctorName": "Hitesh yadav",
    "activityType": "CRM",
    "speciality": "CARDIO",
    "dob": "11/05/1900",
    "doa": "31/01/1900",
    "apr": "1,10,15",
    "may": "8,11,28",
    "jun": "12,22,27",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 76,
    "doctorName": "JAGDISH VISHNOI",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "03/03/1974",
    "doa": "",
    "apr": "14,21,23,28",
    "may": "6,12,19,26",
    "jun": "2,9,16",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 42,
    "doctorName": "JAY CHORDIYA",
    "activityType": "LGT TABLE TOP",
    "speciality": "DM ENDO",
    "dob": "21/04/2019",
    "doa": "",
    "apr": "appointment",
    "may": "",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 56,
    "doctorName": "JAYESH GANDHI",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "10/06/2019",
    "doa": "",
    "apr": "25",
    "may": "2,9,16",
    "jun": "6,10,20,27",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 51,
    "doctorName": "JC DEVPURA",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "30/03/2019",
    "doa": "",
    "apr": "7,13,18",
    "may": "12",
    "jun": "2,13,22,29",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 25,
    "doctorName": "jimesh Pandiya",
    "activityType": "CRM",
    "speciality": "MBBB MD",
    "dob": "22/03/1900",
    "doa": "06/12/1900",
    "apr": "8,16",
    "may": "13,25",
    "jun": "17,26",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 54,
    "doctorName": "JITENA JINGAR",
    "activityType": "",
    "speciality": "MD PSY",
    "dob": "24/09/2019",
    "doa": "",
    "apr": "4,17,23,24,28",
    "may": "4,11,15,27,29",
    "jun": "13,19,24",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 44,
    "doctorName": "JITESH AGRAWAL",
    "activityType": "VTL TABLE TOP",
    "speciality": "MBBB MD",
    "dob": "",
    "doa": "",
    "apr": "appointment",
    "may": "29",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 68,
    "doctorName": "KALPESH CHODHRAY",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 100,
    "doctorName": "KAMLESH BHATT",
    "activityType": "",
    "speciality": "DNB",
    "dob": "",
    "doa": "",
    "apr": "",
    "may": "6,19,26",
    "jun": "2,9,16",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 81,
    "doctorName": "KANTI LAL MEGWAL",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "09/01/2019",
    "doa": "",
    "apr": "25",
    "may": "2,9,16,23",
    "jun": "6,10,20,27",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 35,
    "doctorName": "KAPIL BHARGAV",
    "activityType": "WCFYH VAL/VIN",
    "speciality": "DM CARDIO",
    "dob": "16/12/2019",
    "doa": "",
    "apr": "3,17,24",
    "may": "ntc",
    "jun": "19",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 3,
    "doctorName": "KAVITA BADJATIYA",
    "activityType": "CRM",
    "speciality": "MD MED",
    "dob": "26/08/2019",
    "doa": "",
    "apr": "1,7,13,18,20",
    "may": "4,11,21,27",
    "jun": "9,13,15,22,29",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 64,
    "doctorName": "KB BADAULIA",
    "activityType": "",
    "speciality": "MBBS",
    "dob": "",
    "doa": "",
    "apr": "13",
    "may": "",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 47,
    "doctorName": "KC JAIN",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "24/07/2019",
    "doa": "",
    "apr": "2 times not available ,18",
    "may": "",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 19,
    "doctorName": "KIRIT GANDHI",
    "activityType": "CRM",
    "speciality": "MD MED",
    "dob": "11/07/2019",
    "doa": "",
    "apr": "8,16",
    "may": "na ,25",
    "jun": "17,26",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 78,
    "doctorName": "KN DAS",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "15/11/2019",
    "doa": "",
    "apr": "25",
    "may": "2,9,16,23",
    "jun": "6,10,20,27",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 58,
    "doctorName": "KRIPA SHANKAR",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "15/09/2019",
    "doa": "",
    "apr": "6,22",
    "may": "7,22",
    "jun": "4,23",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 82,
    "doctorName": "LALIT JAINANI",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "11/04/2019",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "11",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 67,
    "doctorName": "LALIT SHREEMALI",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "20/12/2019",
    "doa": "",
    "apr": "3,11,17,24,27",
    "may": "15,29",
    "jun": "19",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 89,
    "doctorName": "M vijay vargiy",
    "activityType": "",
    "speciality": "M B B S PHY",
    "dob": "",
    "doa": "",
    "apr": "6,22",
    "may": "7,22",
    "jun": "4,23",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 83,
    "doctorName": "MADHUP BAXI",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "29/01/2019",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "11",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 1,
    "doctorName": "MAHESH DAVE",
    "activityType": "CRM",
    "speciality": "MD MED",
    "dob": "03/03/2019",
    "doa": "",
    "apr": "1,10,17",
    "may": "15,19,26,30",
    "jun": "na,13,25,30",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 122,
    "doctorName": "MAHESH DESAI",
    "activityType": "",
    "speciality": "DNB NEFRO",
    "dob": "",
    "doa": "",
    "apr": "3,17",
    "may": "4,29",
    "jun": "13,15",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 40,
    "doctorName": "MAHESH JAIN",
    "activityType": "A2 GHEE",
    "speciality": "CARDIO",
    "dob": "",
    "doa": "",
    "apr": "28",
    "may": "",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 93,
    "doctorName": "Manish Khandelwal",
    "activityType": "",
    "speciality": "MBBS MD",
    "dob": "",
    "doa": "",
    "apr": "6,22",
    "may": "7,22",
    "jun": "4,23",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 43,
    "doctorName": "MANISH KULSHERT",
    "activityType": "VTL TABLE TOP",
    "speciality": "DM NEURO",
    "dob": "",
    "doa": "",
    "apr": "4,7,9,13,18,24",
    "may": "11,15",
    "jun": "2,25",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 13,
    "doctorName": "MANU SHARMA",
    "activityType": "CRM",
    "speciality": "MD PSY",
    "dob": "05/12/2019",
    "doa": "",
    "apr": "4,17,24",
    "may": "4,15,27,29",
    "jun": "15,19",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 98,
    "doctorName": "MAYANK SHARMA",
    "activityType": "",
    "speciality": "medicine",
    "dob": "",
    "doa": "",
    "apr": "8,16",
    "may": "13,25",
    "jun": "17,26",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 88,
    "doctorName": "MK MEENA",
    "activityType": "",
    "speciality": "SURJAN",
    "dob": "",
    "doa": "",
    "apr": "6",
    "may": "7",
    "jun": "4",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 30,
    "doctorName": "Mona dingra",
    "activityType": "WCFYH VTL",
    "speciality": "ENDO",
    "dob": "18/07/1900",
    "doa": "10/02/1900",
    "apr": "out of Town ,18,23",
    "may": "21,28",
    "jun": "22",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 53,
    "doctorName": "MUKESH BARJATIYA",
    "activityType": "",
    "speciality": "DNB NEFRO",
    "dob": "",
    "doa": "",
    "apr": "",
    "may": "12,19,27",
    "jun": "3,15",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 33,
    "doctorName": "MUKESH SHARMA",
    "activityType": "WCFYH VAL/VIN",
    "speciality": "DM CARDIO",
    "dob": "07/07/2019",
    "doa": "",
    "apr": "2,21,29",
    "may": "12,19",
    "jun": "3,24",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 70,
    "doctorName": "NAMAN N TANEJA",
    "activityType": "",
    "speciality": "",
    "dob": "",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "27",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 4,
    "doctorName": "NAVGEET MATHUR",
    "activityType": "CRM",
    "speciality": "MD MED",
    "dob": "",
    "doa": "",
    "apr": "3,11",
    "may": "na out of town",
    "jun": "na,13,19",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 91,
    "doctorName": "Navneet patel kiyda",
    "activityType": "",
    "speciality": "MBBB MD",
    "dob": "30/06/1900",
    "doa": "23/04/1900",
    "apr": "8,16",
    "may": "13,25",
    "jun": "17,26",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 73,
    "doctorName": "NEHA SHARMA",
    "activityType": "",
    "speciality": "",
    "dob": "",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "19",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 46,
    "doctorName": "Nilesh pathira",
    "activityType": "GLUCOMETER",
    "speciality": "M B B S PHY",
    "dob": "28/01/1900",
    "doa": "14/04/1900",
    "apr": "appointment ,28",
    "may": "12,19,26",
    "jun": "2,ntc",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 69,
    "doctorName": "OP MEENA",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 5,
    "doctorName": "PARAS JAIN",
    "activityType": "CRM",
    "speciality": "MD MED",
    "dob": "23/11/2019",
    "doa": "",
    "apr": "4,15,24",
    "may": "14,26",
    "jun": "1,24",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 90,
    "doctorName": "pintu aahari",
    "activityType": "",
    "speciality": "MBBB MD",
    "dob": "",
    "doa": "",
    "apr": "25",
    "may": "2,9,16,23",
    "jun": "6,10,27",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 60,
    "doctorName": "PRASHANT BADJATIYA",
    "activityType": "",
    "speciality": "CONSULTANT PHYSICIAN",
    "dob": "",
    "doa": "",
    "apr": "7,13,18,20",
    "may": "4,11,14,27",
    "jun": "9,12,22",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 99,
    "doctorName": "PRATIBHA CHOUDHURY",
    "activityType": "",
    "speciality": "PHY",
    "dob": "",
    "doa": "",
    "apr": "1,15,20",
    "may": "11,27",
    "jun": "12,15,18,29",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 110,
    "doctorName": "Praveen jain",
    "activityType": "",
    "speciality": "MBBS",
    "dob": "",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "10",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 105,
    "doctorName": "Prerna baheti",
    "activityType": "",
    "speciality": "MBBS,DNB,ECMO",
    "dob": "",
    "doa": "",
    "apr": "4,17",
    "may": "14,19",
    "jun": "27",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 77,
    "doctorName": "PRERNA BHARGAV",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "23/03/2019",
    "doa": "",
    "apr": "9",
    "may": "21",
    "jun": "24",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 29,
    "doctorName": "PRIYANKA MINOCHA",
    "activityType": "WCFYH VTL",
    "speciality": "MBBS,DNB,ECMO",
    "dob": "",
    "doa": "",
    "apr": "3,17,24",
    "may": "8,19,29",
    "jun": "12",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 106,
    "doctorName": "R N LADHA",
    "activityType": "",
    "speciality": "MS ORTHO",
    "dob": "",
    "doa": "",
    "apr": "",
    "may": "21",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 17,
    "doctorName": "RAHUL PANCHAL",
    "activityType": "CRM",
    "speciality": "MD MED",
    "dob": "21/04/2019",
    "doa": "",
    "apr": "25",
    "may": "2,9,16,23",
    "jun": "10,20,27,",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 62,
    "doctorName": "rahul sehlot",
    "activityType": "",
    "speciality": "ENDO",
    "dob": "",
    "doa": "",
    "apr": "3,15",
    "may": "29",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 117,
    "doctorName": "RAJENDRA KUMAR SAMAR",
    "activityType": "",
    "speciality": "PHY",
    "dob": "",
    "doa": "",
    "apr": "3,24",
    "may": "",
    "jun": "12",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 71,
    "doctorName": "RAJESH KHOIWAL",
    "activityType": "",
    "speciality": "DM NEURO",
    "dob": "",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 89,
    "doctorName": "RAKESH MEENA",
    "activityType": "",
    "speciality": "",
    "dob": "",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "6,10,20,27",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 80,
    "doctorName": "RAJESH SIROIYA",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "04/10/2019",
    "doa": "",
    "apr": "25",
    "may": "2,9,16,23",
    "jun": "6,10,20,27",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 11,
    "doctorName": "RAMESH PATEL",
    "activityType": "CRM",
    "speciality": "DM CARDIO",
    "dob": "30/09/2019",
    "doa": "",
    "apr": "1,17,22",
    "may": "8,15,18,19,29",
    "jun": "12,19,24",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 104,
    "doctorName": "RAMKUMAR DAKSH",
    "activityType": "",
    "speciality": "GP",
    "dob": "",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "11",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 121,
    "doctorName": "RAVI KUMAR  MANGLANI",
    "activityType": "",
    "speciality": "MBBB MD",
    "dob": "",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 95,
    "doctorName": "Ravi Mangalia",
    "activityType": "",
    "speciality": "CONSULTANT PHY",
    "dob": "",
    "doa": "",
    "apr": "3,17,22",
    "may": "8,15,29",
    "jun": "13,19,20,27",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 18,
    "doctorName": "RK MALOT",
    "activityType": "CRM",
    "speciality": "MD MED",
    "dob": "09/05/2019",
    "doa": "",
    "apr": "8,16",
    "may": "13,25",
    "jun": "17,26",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 55,
    "doctorName": "RK SHARMA",
    "activityType": "",
    "speciality": "DM ENDO",
    "dob": "14/01/2019",
    "doa": "",
    "apr": "na,14,21,28",
    "may": "6,12,19,26",
    "jun": "9,16",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 115,
    "doctorName": "RL MEENA",
    "activityType": "",
    "speciality": "C.PHY",
    "dob": "",
    "doa": "",
    "apr": "7,23",
    "may": "4",
    "jun": "22,25",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 39,
    "doctorName": "S K KUASHIK",
    "activityType": "A2 GHEE",
    "speciality": "DM CARDIO",
    "dob": "",
    "doa": "",
    "apr": "2,17,27",
    "may": "6,27",
    "jun": "na,13,24",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 118,
    "doctorName": "S.A.BOHRA",
    "activityType": "",
    "speciality": "MBBS MD",
    "dob": "",
    "doa": "",
    "apr": "na,21,28",
    "may": "12,19,26",
    "jun": "2,9,16",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 48,
    "doctorName": "SAFDAR HUSSAIN",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "05/05/2019",
    "doa": "",
    "apr": "7,13",
    "may": "4,11,18",
    "jun": "1,15,22,25,29",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 49,
    "doctorName": "SALMA SHAH",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "07/03/2019",
    "doa": "",
    "apr": "2,10,17,23,24,30",
    "may": "8,15",
    "jun": "12,18,25",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 16,
    "doctorName": "SANDEEP BHATNAGAR",
    "activityType": "CRM",
    "speciality": "MD MED",
    "dob": "13/02/2019",
    "doa": "",
    "apr": "2,15,27",
    "may": "21",
    "jun": "15",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 101,
    "doctorName": "SANDEEP CHANDOLIYA",
    "activityType": "",
    "speciality": "MBBB MD",
    "dob": "",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "11",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 8,
    "doctorName": "SANDEEP KANSARA",
    "activityType": "CRM+LGT TABLE TOP",
    "speciality": "DM ENDO",
    "dob": "22/10/2019",
    "doa": "",
    "apr": "11,23",
    "may": "14,21",
    "jun": "2,9,24",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 36,
    "doctorName": "Sanjay Gandhi",
    "activityType": "WCFYH VAL/VIN",
    "speciality": "C V T S",
    "dob": "",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "13",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 45,
    "doctorName": "SATISH CHOUDHARY",
    "activityType": "VTL TABLE TOP",
    "speciality": "PHYSCIAN",
    "dob": "",
    "doa": "",
    "apr": "6,22",
    "may": "7,22",
    "jun": "23",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 119,
    "doctorName": "SHRAVAN KUMAR MEENA",
    "activityType": "",
    "speciality": "MBBS",
    "dob": "",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 84,
    "doctorName": "SHUSHIL CHOUHAN",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "17/02/2019",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "4,23",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 15,
    "doctorName": "SUMIT SIROIYA",
    "activityType": "CRM",
    "speciality": "MD MED",
    "dob": "14/01/2019",
    "doa": "",
    "apr": "na,18",
    "may": "",
    "jun": "12",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 85,
    "doctorName": "SUNIL UPADHAY",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "07/02/2019",
    "doa": "",
    "apr": "6,22",
    "may": "22",
    "jun": "4",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 94,
    "doctorName": "SURAJ GUPTA",
    "activityType": "",
    "speciality": "NEPHROLOGIST",
    "dob": "",
    "doa": "",
    "apr": "3,na",
    "may": "8,15",
    "jun": "13,19",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 26,
    "doctorName": "Suresh Chandra",
    "activityType": "CRM",
    "speciality": "GEN MED",
    "dob": "",
    "doa": "",
    "apr": "na",
    "may": "",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 73,
    "doctorName": "TARUN MATHUR",
    "activityType": "",
    "speciality": "DM NEURO",
    "dob": "02/08/1979",
    "doa": "",
    "apr": "24",
    "may": "5",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 52,
    "doctorName": "TARUN RHLOT",
    "activityType": "",
    "speciality": "DM NEURO",
    "dob": "",
    "doa": "",
    "apr": "appointment",
    "may": "",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 31,
    "doctorName": "UDAY BHOMIK",
    "activityType": "WCFYH VTL",
    "speciality": "DM NEURO",
    "dob": "08/04/2019",
    "doa": "",
    "apr": "na,30",
    "may": "15",
    "jun": "12",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 14,
    "doctorName": "VIJAY GOYAL",
    "activityType": "CRM",
    "speciality": "MD MED",
    "dob": "01/09/2019",
    "doa": "",
    "apr": "4,15",
    "may": "14",
    "jun": "1",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 41,
    "doctorName": "Vinod bokadia",
    "activityType": "LGT TABLE TOP",
    "speciality": "Diabet/ End",
    "dob": "24/02/1988",
    "doa": "02/05/2014",
    "apr": "28",
    "may": "6,28",
    "jun": "19,20,27",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 28,
    "doctorName": "VINOD KUMAR RAI",
    "activityType": "CRM",
    "speciality": "MBBS",
    "dob": "",
    "doa": "",
    "apr": "2,10,17,23,24,30",
    "may": "8,15,21,28",
    "jun": "12,18,25",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 9,
    "doctorName": "VINOD MEHTA",
    "activityType": "CRM",
    "speciality": "DM NEURO",
    "dob": "02/06/2019",
    "doa": "",
    "apr": "2,3,11,17",
    "may": "14,15,26,29",
    "jun": "na,16,18,19,29",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 102,
    "doctorName": "VK RAMCHANDANI",
    "activityType": "",
    "speciality": "General Practitioner (GP)",
    "dob": "",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 109,
    "doctorName": "YASH SHAH",
    "activityType": "",
    "speciality": "CONS PHY",
    "dob": "",
    "doa": "",
    "apr": "8,16",
    "may": "13,25",
    "jun": "17,26",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 63,
    "doctorName": "YN VERMA",
    "activityType": "",
    "speciality": "MD MED",
    "dob": "03/07/2019",
    "doa": "",
    "apr": "",
    "may": "11",
    "jun": "22",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  },
  {
    "srNo": 112,
    "doctorName": "YOGENDRA SINGH RANAWAT",
    "activityType": "",
    "speciality": "MD CARDIO",
    "dob": "",
    "doa": "",
    "apr": "",
    "may": "",
    "jun": "",
    "jul": "",
    "aug": "",
    "sept": "",
    "oct": "",
    "nov": "",
    "dec": "",
    "jan": "",
    "feb": "",
    "mar": ""
  }
];

export const MslSheet: React.FC = () => {
  const [search, setSearch] = useState('');
  const [doctors, setDoctors] = useState<MslDoctor[]>(() => {
    if (memoryStore.mslData) {
      return memoryStore.mslData;
    }
    return FULL_123_MSL_DOCTORS;
  });

  // Column Visibility Toggles (Can be hidden to save space)
  const [showActivity, setShowActivity] = useState(true);
  const [showSpeciality, setShowSpeciality] = useState(true);
  const [showDob, setShowDob] = useState(true);
  const [showDoa, setShowDoa] = useState(true);

  const [savedSuccess, setSavedSuccess] = useState(false);

  // Compact Column Widths (in pixels)
  const W_SR = 38;
  const W_DOC = 145;
  const W_ACT = 90;
  const W_SPEC = 110;
  const W_DOB = 75;
  const W_DOA = 75;

  // Calculate Dynamic Sticky Offsets
  let currentOffset = W_SR + W_DOC;
  const offsetAct = currentOffset;
  if (showActivity) currentOffset += W_ACT;
  const offsetSpec = currentOffset;
  if (showSpeciality) currentOffset += W_SPEC;
  const offsetDob = currentOffset;
  if (showDob) currentOffset += W_DOB;
  const offsetDoa = currentOffset;

  // Determine which column is the last visible left column (gets the cyan divider)
  let lastLeftCol = 'doa';
  if (!showDoa) {
    if (showDob) lastLeftCol = 'dob';
    else if (showSpeciality) lastLeftCol = 'speciality';
    else if (showActivity) lastLeftCol = 'activity';
    else lastLeftCol = 'doctor';
  }

  const isAllHidden = !showActivity && !showSpeciality && !showDob && !showDoa;

  const toggleFocusMode = () => {
    if (isAllHidden) {
      setShowActivity(true);
      setShowSpeciality(true);
      setShowDob(true);
      setShowDoa(true);
    } else {
      setShowActivity(false);
      setShowSpeciality(false);
      setShowDob(false);
      setShowDoa(false);
    }
  };

  const handleFieldChange = (srNo: number, field: keyof MslDoctor, val: string) => {
    setDoctors(prev => {
      const updated = prev.map(d => d.srNo === srNo ? { ...d, [field]: val } : d);
      memoryStore.mslData = updated;
      return updated;
    });
  };

  const handleAddDoctor = () => {
    setDoctors(prev => {
      const nextSr = prev.length > 0 ? Math.max(...prev.map(p => p.srNo)) + 1 : 1;
      const updated = [
        ...prev,
        { srNo: nextSr, doctorName: '', activityType: '', speciality: '', dob: '', doa: '', apr: '', may: '', jun: '', jul: '', aug: '', sept: '', oct: '', nov: '', dec: '', jan: '', feb: '', mar: '' }
      ];
      memoryStore.mslData = updated;
      return updated;
    });
  };

  const handleDeleteDoctor = (srNo: number) => {
    setDoctors(prev => {
      const updated = prev.filter(d => d.srNo !== srNo);
      memoryStore.mslData = updated;
      return updated;
    });
  };

  const handleSave = () => {
    memoryStore.mslData = doctors;
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 2000);
  };

  const handleExportCSV = () => {
    let csv = `,,,,,,VISIT DATES,,,,,,,,,,\n`;
    csv += `SrNo,Doctor Name,Activity Type,Speciality,DOB,DOA,APR,MAY,JUN,JUL,AUG,SEPT,OCT,NOV,DEC,JAN,FEB,MAR\n`;
    
    doctors.forEach(d => {
      csv += `${d.srNo},"${d.doctorName}","${d.activityType}","${d.speciality}","${d.dob}","${d.doa}","${d.apr}","${d.may}","${d.jun}","${d.jul}","${d.aug}","${d.sept}","${d.oct}","${d.nov}","${d.dec}","${d.jan}","${d.feb}","${d.mar}"\n`;
    });

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', '14_MSL.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const filtered = doctors.filter(d => 
    d.doctorName.toLowerCase().includes(search.toLowerCase()) || 
    d.speciality.toLowerCase().includes(search.toLowerCase()) ||
    d.activityType.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 md:p-5 shadow-xl space-y-4">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <span className="p-2 bg-cyan-500/20 text-cyan-400 rounded-lg"><Calendar size={18} /></span>
          <div>
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              14. MSL (Master Specialty List &amp; Visit Dates)
              <span className="text-[10px] bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 px-2 py-0.5 rounded-full font-mono font-bold">
                SYSTEM V56.0 • COMPACT &amp; HIDE TOGGLES
              </span>
            </h2>
            <p className="text-xs text-slate-400">Total {doctors.length} Doctors • Compact Left Columns with Custom Column Hiding</p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <div className="relative w-full sm:w-52">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
            <input 
              type="text" 
              placeholder="Search doctor, speciality..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-8 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
            />
          </div>

          <button
            onClick={handleAddDoctor}
            className="flex items-center gap-1 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-cyan-300 rounded-xl text-xs font-semibold transition cursor-pointer"
          >
            <Plus size={14} /> Add Doctor
          </button>

          <button
            onClick={handleSave}
            className="flex items-center gap-1.5 px-3.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-xl text-xs font-semibold transition cursor-pointer"
          >
            {savedSuccess ? <Check size={14} className="text-emerald-400" /> : <Save size={14} />}
            {savedSuccess ? 'Saved' : 'Save'}
          </button>

          <button
            onClick={handleExportCSV}
            className="flex items-center gap-1.5 px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold transition cursor-pointer"
          >
            <Download size={14} /> Export CSV
          </button>
        </div>
      </div>

      {/* COLUMN HIDE / SHOW CONTROLS BAR (IPAD FRIENDLY) */}
      <div className="flex flex-wrap items-center justify-between gap-2 p-2.5 bg-slate-950 rounded-xl border border-slate-800 text-xs">
        <div className="flex flex-wrap items-center gap-1.5">
          <span className="text-[11px] font-bold text-slate-400 uppercase mr-1 flex items-center gap-1">
            <Filter size={13} className="text-cyan-400" /> Show/Hide Columns:
          </span>

          <button
            onClick={() => setShowActivity(!showActivity)}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold border transition cursor-pointer flex items-center gap-1 ${
              showActivity 
                ? 'bg-amber-500/20 text-amber-300 border-amber-500/40' 
                : 'bg-slate-900 text-slate-500 border-slate-800 hover:text-slate-300'
            }`}
          >
            {showActivity ? <Eye size={12} /> : <EyeOff size={12} />} Activity
          </button>

          <button
            onClick={() => setShowSpeciality(!showSpeciality)}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold border transition cursor-pointer flex items-center gap-1 ${
              showSpeciality 
                ? 'bg-blue-500/20 text-blue-300 border-blue-500/40' 
                : 'bg-slate-900 text-slate-500 border-slate-800 hover:text-slate-300'
            }`}
          >
            {showSpeciality ? <Eye size={12} /> : <EyeOff size={12} />} Speciality
          </button>

          <button
            onClick={() => setShowDob(!showDob)}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold border transition cursor-pointer flex items-center gap-1 ${
              showDob 
                ? 'bg-purple-500/20 text-purple-300 border-purple-500/40' 
                : 'bg-slate-900 text-slate-500 border-slate-800 hover:text-slate-300'
            }`}
          >
            {showDob ? <Eye size={12} /> : <EyeOff size={12} />} DOB
          </button>

          <button
            onClick={() => setShowDoa(!showDoa)}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold border transition cursor-pointer flex items-center gap-1 ${
              showDoa 
                ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40' 
                : 'bg-slate-900 text-slate-500 border-slate-800 hover:text-slate-300'
            }`}
          >
            {showDoa ? <Eye size={12} /> : <EyeOff size={12} />} DOA
          </button>
        </div>

        {/* ⚡ Focus Mode Toggle (Hide all extra details at once) */}
        <button
          onClick={toggleFocusMode}
          className={`px-3 py-1 rounded-lg text-xs font-bold border transition cursor-pointer flex items-center gap-1.5 shadow-sm ${
            isAllHidden 
              ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white border-cyan-400 shadow-cyan-950' 
              : 'bg-slate-900 text-amber-300 border-amber-500/40 hover:bg-amber-950/40'
          }`}
        >
          <Sparkles size={13} className="text-yellow-300" />
          {isAllHidden ? 'Show All Columns' : '⚡ Focus Mode (Doctor + Months Only)'}
        </button>
      </div>

      {/* TABLE WITH DYNAMIC STICKY FROZEN PANES */}
      <div className="overflow-x-auto max-h-[640px] border border-slate-800 rounded-2xl relative shadow-2xl">
        <table className="w-full text-left text-xs border-separate border-spacing-0">
          <thead className="sticky top-0 z-40 bg-slate-950">
            <tr>
              {/* 1. SrNo */}
              <th 
                style={{ width: `${W_SR}px`, minWidth: `${W_SR}px`, left: 0 }}
                className="p-2 text-center bg-slate-950 border-b border-r border-slate-800 sticky z-50 text-slate-400 font-bold uppercase"
              >
                #
              </th>

              {/* 2. Doctor Name */}
              <th 
                style={{ width: `${W_DOC}px`, minWidth: `${W_DOC}px`, left: `${W_SR}px` }}
                className={`p-2 bg-slate-950 border-b border-slate-800 sticky z-50 text-slate-400 font-bold uppercase ${
                  lastLeftCol === 'doctor' ? 'border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)]' : 'border-r'
                }`}
              >
                Doctor Name
              </th>

              {/* 3. Activity Type (Toggleable) */}
              {showActivity && (
                <th 
                  style={{ width: `${W_ACT}px`, minWidth: `${W_ACT}px`, left: `${offsetAct}px` }}
                  className={`p-2 bg-slate-950 border-b border-slate-800 sticky z-50 text-amber-400 font-bold uppercase ${
                    lastLeftCol === 'activity' ? 'border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)]' : 'border-r'
                  }`}
                >
                  Activity
                </th>
              )}

              {/* 4. Speciality (Toggleable) */}
              {showSpeciality && (
                <th 
                  style={{ width: `${W_SPEC}px`, minWidth: `${W_SPEC}px`, left: `${offsetSpec}px` }}
                  className={`p-2 bg-slate-950 border-b border-slate-800 sticky z-50 text-blue-300 font-bold uppercase ${
                    lastLeftCol === 'speciality' ? 'border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)]' : 'border-r'
                  }`}
                >
                  Speciality
                </th>
              )}

              {/* 5. DOB (Toggleable) */}
              {showDob && (
                <th 
                  style={{ width: `${W_DOB}px`, minWidth: `${W_DOB}px`, left: `${offsetDob}px` }}
                  className={`p-2 text-center bg-slate-950 border-b border-slate-800 sticky z-50 text-purple-300 font-bold uppercase ${
                    lastLeftCol === 'dob' ? 'border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)]' : 'border-r'
                  }`}
                >
                  DOB
                </th>
              )}

              {/* 6. DOA (Toggleable with Divider) */}
              {showDoa && (
                <th 
                  style={{ width: `${W_DOA}px`, minWidth: `${W_DOA}px`, left: `${offsetDoa}px` }}
                  className="p-2 text-center bg-slate-950 border-b border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)] sticky z-50 text-emerald-400 font-bold uppercase"
                >
                  DOA
                </th>
              )}

              {/* 12 Expanded Month Columns (160px) */}
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-cyan-400 font-bold uppercase">APR</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-emerald-400 font-bold uppercase">MAY</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-purple-400 font-bold uppercase">JUN</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-blue-400 font-bold uppercase">JUL</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-amber-400 font-bold uppercase">AUG</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-rose-400 font-bold uppercase">SEPT</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-cyan-300 font-bold uppercase">OCT</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-emerald-300 font-bold uppercase">NOV</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-purple-300 font-bold uppercase">DEC</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-blue-300 font-bold uppercase">JAN</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-amber-300 font-bold uppercase">FEB</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-rose-300 font-bold uppercase">MAR</th>
              <th className="p-2.5 text-center w-[50px] min-w-[50px] bg-slate-950 border-b border-slate-800 text-slate-400 font-bold uppercase">Action</th>
            </tr>
          </thead>
          <tbody className="bg-slate-900">
            {filtered.map(doc => (
              <tr key={doc.srNo} className="hover:bg-slate-800/60 transition group">
                {/* 1. SrNo */}
                <td 
                  style={{ width: `${W_SR}px`, minWidth: `${W_SR}px`, left: 0 }}
                  className="p-1.5 text-center text-slate-400 font-mono border-b border-r border-slate-800/80 sticky bg-slate-900 group-hover:bg-slate-800 z-20 text-xs"
                >
                  {doc.srNo}
                </td>

                {/* 2. Doctor Name */}
                <td 
                  style={{ width: `${W_DOC}px`, minWidth: `${W_DOC}px`, left: `${W_SR}px` }}
                  className={`p-1 border-b border-slate-800/80 sticky bg-slate-900 group-hover:bg-slate-800 z-20 ${
                    lastLeftCol === 'doctor' ? 'border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)]' : 'border-r'
                  }`}
                >
                  <input
                    type="text"
                    value={doc.doctorName}
                    onChange={e => handleFieldChange(doc.srNo, 'doctorName', e.target.value)}
                    className="w-full py-1 px-1.5 bg-slate-950 rounded-md font-bold text-white border border-slate-800 focus:border-cyan-500 focus:outline-none text-[11px]"
                  />
                </td>

                {/* 3. Activity Type (Toggleable) */}
                {showActivity && (
                  <td 
                    style={{ width: `${W_ACT}px`, minWidth: `${W_ACT}px`, left: `${offsetAct}px` }}
                    className={`p-1 border-b border-slate-800/80 sticky bg-slate-900 group-hover:bg-slate-800 z-20 ${
                      lastLeftCol === 'activity' ? 'border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)]' : 'border-r'
                    }`}
                  >
                    <input
                      type="text"
                      value={doc.activityType}
                      onChange={e => handleFieldChange(doc.srNo, 'activityType', e.target.value)}
                      placeholder="-"
                      className="w-full py-1 px-1.5 bg-slate-950 rounded-md text-amber-400 border border-slate-800 focus:border-cyan-500 focus:outline-none text-[10px] font-semibold"
                    />
                  </td>
                )}

                {/* 4. Speciality (Toggleable) */}
                {showSpeciality && (
                  <td 
                    style={{ width: `${W_SPEC}px`, minWidth: `${W_SPEC}px`, left: `${offsetSpec}px` }}
                    className={`p-1 border-b border-slate-800/80 sticky bg-slate-900 group-hover:bg-slate-800 z-20 ${
                      lastLeftCol === 'speciality' ? 'border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)]' : 'border-r'
                    }`}
                  >
                    <input
                      type="text"
                      value={doc.speciality}
                      onChange={e => handleFieldChange(doc.srNo, 'speciality', e.target.value)}
                      placeholder="-"
                      className="w-full py-1 px-1.5 bg-slate-950 rounded-md text-slate-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-[10px]"
                    />
                  </td>
                )}

                {/* 5. DOB (Toggleable) */}
                {showDob && (
                  <td 
                    style={{ width: `${W_DOB}px`, minWidth: `${W_DOB}px`, left: `${offsetDob}px` }}
                    className={`p-1 border-b border-slate-800/80 sticky bg-slate-900 group-hover:bg-slate-800 z-20 ${
                      lastLeftCol === 'dob' ? 'border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)]' : 'border-r'
                    }`}
                  >
                    <input
                      type="text"
                      value={doc.dob}
                      onChange={e => handleFieldChange(doc.srNo, 'dob', e.target.value)}
                      placeholder="DD/MM/YYYY"
                      className="w-full py-1 px-1 bg-slate-950 rounded-md font-mono text-slate-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-center text-[10px]"
                    />
                  </td>
                )}

                {/* 6. DOA (Toggleable with Divider) */}
                {showDoa && (
                  <td 
                    style={{ width: `${W_DOA}px`, minWidth: `${W_DOA}px`, left: `${offsetDoa}px` }}
                    className="p-1 border-b border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)] sticky bg-slate-900 group-hover:bg-slate-800 z-20"
                  >
                    <input
                      type="text"
                      value={doc.doa}
                      onChange={e => handleFieldChange(doc.srNo, 'doa', e.target.value)}
                      placeholder="DD/MM/YYYY"
                      className="w-full py-1 px-1 bg-slate-950 rounded-md font-mono text-slate-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-center text-[10px] font-bold"
                    />
                  </td>
                )}

                {/* 12 Months (160px Wide Inputs) */}
                {['apr', 'may', 'jun', 'jul', 'aug', 'sept', 'oct', 'nov', 'dec', 'jan', 'feb', 'mar'].map(monthKey => (
                  <td key={monthKey} className="p-1.5 w-[160px] min-w-[160px] border-b border-r border-slate-800/50">
                    <input
                      type="text"
                      value={(doc as any)[monthKey]}
                      onChange={e => handleFieldChange(doc.srNo, monthKey as any, e.target.value)}
                      placeholder="-"
                      className="w-full py-1.5 px-2 bg-slate-950 rounded-lg font-mono text-slate-100 border border-slate-800 focus:border-cyan-400 focus:bg-slate-900 focus:outline-none text-center text-xs font-semibold"
                    />
                  </td>
                ))}

                {/* Action */}
                <td className="p-1 text-center border-b border-slate-800/80 w-[50px] min-w-[50px]">
                  <button
                    type="button"
                    onClick={() => handleDeleteDoctor(doc.srNo)}
                    className="p-1.5 text-slate-500 hover:text-rose-400 rounded-lg transition cursor-pointer"
                  >
                    <Trash2 size={14} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
