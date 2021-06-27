"""
Prime Minister, I must protest in the strongest possible terms my profound opposition to a newly instituted practice which imposes severe and intolerable restrictions upon the ingress and egress of senior members of the hierarchy and which will, in all probability, should the current deplorable innovation be perpetuated, precipitate a constriction of the channels of communication, and culminate in a condition of organisational atrophy and administrative paralysis which will render effectively impossible the coherent and co-ordinated discharge of the function of government within Her Majesty's United Kingdom of Great Britain and Northern Ireland.
"""
from manimlib import *

class Lines(Scene):
    def construct(self):
        text = TexText(r"Prime Minister, I must protest in the strongest possible terms \\my profound opposition to a newly instituted practice \\which imposes severe and intolerable restrictions \\upon the ingress and egress of senior members of the hierarchy \\and which will, in all probability, \\should the current deplorable innovation be perpetuated, \\precipitate a constriction of the channels of communication, \\and culminate in a condition of \\organisational atrophy and administrative paralysis \\which will render effectively impossible the coherent \\and co-ordinated discharge of the function of government \\within Her Majesty's United Kingdom of Great Britain \\and Northern Ireland.")
        self.add(text)