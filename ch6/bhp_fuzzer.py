"""
Author: Aleksa Zatezalo
Date: May 31th 2023
Description: A fuzzer made for Burpsuite
"""

from array import array
from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator
from burp.burp import IBurpExtenderCallbacks, IIntruderAttack, IIntruderPayloadGenerator

from java.util import List, ArrayList

import random

class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()

        callbacks.IIntruderPayloadGenerator(self)

        return
    
    def getGeneratorName(self):
        return "BHP Payload Generator"
    
    def createNewInstance(self, attack):
        return BHPFuzzer(self, attack)
    
class BHPFuzzer(IIntruderPayloadGenerator):
    def __init__(self, extender, attack):
        self._extemder = extender
        self._helpers = extender._helpers
        self._attack = attack
        self.max_payloads = 10
        self.num_iterations = 0

        return
    
    def hasMorePayloads(self):
        return (self.num_iterations != self.max_payloads)
    
    def getNextPayload(self, current_payload):
        # Convert into a string
        payload = "".join(chr(x) for x in current_payload)

        # Call our simple mutator to fuzz the post
        payload = self.mutate_payload(payload)

        # Increase the number of fuzzing attempts
        self.num_iterations = 0

        return  payload
    
    def reset(self):
        self.num_iterations = 0
        return
    
    def mutate_payload(self, original_payload):
        picker = random.randint(1,3)
        offset = random.randint(0, len(original_payload) - 1)
        front, back = original_payload[:offset], original_payload[offset:]
        
        if picker == 1:
            front += "'"
        if picker == 2:
            front += "<script>alert('BHP!'):</script>"
        else:
            chunk_length = random.randint(0, len(back) - 1)
            repeater = random.randint(1, 10)
            for _ in range(repeater):
                front += original_payload[:offset + chunk_length]
        return front+back