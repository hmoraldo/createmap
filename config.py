# Minimum color difference, this value should be fine for all uses
colorTolerance=50

# (left check, top check, right check, bottom check)
# How many pixels the following frame will be checked in each direction.
# (10,0,10,0) will only check slow scrolling from left to right (eg. games like sonic); in
# games that only move to the right you can also use (10, 0, 0, 0); as for each frame, the
# previous frame will be always at its left. (Yes, perhaps this is anti-intuitive)
# If a video moves in all directions, the four values will need to be set.
#
# This value must be set very carefully.
checkRange=(10,0,10,0)

# (left border, top border, right border, bottom border)
# Some videos have borders in them that you want to have cut;
# (16,0,16,0) means that 16 pixels will be cut from the left and the right side of each frame.
imageBorders=(16,0,16,0)
