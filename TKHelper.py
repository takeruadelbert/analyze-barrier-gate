# -*- coding: utf-8 -*-
class TKHelper:        
    def PrintDataResult(self, data):
        for val in data:
            print(val, end=" ")
            
    def ConvertDetailTimeToString(self, str_time):
        result = ""
        temp = str_time.split(':')
        hour = int(temp[0])
        minute = int(temp[1])
        second_micro = temp[2]
        temp2 = second_micro.split('.')
        second = int(temp2[0])
        microsecond = "1" + temp2[1]
        millisecond = int(microsecond) / 1000 # 1 microsecond equals 1/1000 millisecond
        
        if hour > 0:
            result += hour + " hour "
        elif minute > 0:
            result += minute + " min "
        result += second + " sec " + millisecond + " msec"
        return result
        