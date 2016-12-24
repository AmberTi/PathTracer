"""pathtracer"""
from collatex import *
collation = Collation()
collation.add_plain_witness("A", "The quick brown fox jumps over the dog")
collation.add_plain_witness("B", "The brown fox jumps over the lazy dog.")

alignment_table = collate(collation)
print(alignment_table)
