#!/usr/bin/env python

import os
import sys
import time

import cv2
import numpy as np

import board
import controller
import imgUtils
import screenshot as screen
from space import Piece

MOVE_WAIT = 0
CLEAR_WAIT = 0.1

def run(brain):
  print '[emulator.py] Running game...'

  for i in xrange(100):
    #controller.MASH_UP()
    controller.MASH_LEFT()
    screenshot = screen.takeScreenshot()
    if screenshot == None:
      time.sleep(MOVE_WAIT)
      continue
    if imgUtils.gameHasEnded(screenshot):
      break
    grid = imgUtils.cropBoard2Player(screenshot)

    controller.MASH_DOWN()

    # Generate board model.
    inputRows = [[-1] * board.WIDTH for _ in range(board.HEIGHT)]
    for square, rowIndex, colIndex in imgUtils.parseSquaresFromBoard(grid):
      val, score = imgUtils.getSquareClassification(square)
      inputRows[rowIndex][colIndex] = Piece(val)

    # Get next action and perform.
    b = board.Board(inputRows=inputRows)
    b.printBoard()
    moves = brain.getNextMoves(b)
    print moves
    cursor_pos = performMoves(moves, (0, 0))

    # End loop.
  print '[emulator.py] Done running game.'

def performMoves(moves, cursor_pos):
  for move in moves:
    next_pos, clear = move
    row_delta, col_delta = (next_pos[0] - cursor_pos[0], next_pos[1] - cursor_pos[1])
    if row_delta > 0:
      #for _ in range(row_delta): controller.MAIN_UP()
      for _ in range(row_delta): controller.D_UP()
    elif row_delta < 0:
      for _ in range(-row_delta): controller.MAIN_DOWN()
      #for _ in range(-row_delta): controller.D_DOWN()
    if col_delta > 0:
      #for _ in range(col_delta): controller.MAIN_RIGHT()
      for _ in range(col_delta): controller.D_RIGHT()
    elif col_delta < 0:
      #for _ in range(-col_delta): controller.MAIN_LEFT()
      for _ in range(-col_delta): controller.D_LEFT()
    cursor_pos = next_pos
    controller.A()
    time.sleep(MOVE_WAIT)
    if clear:
      time.sleep(clear * CLEAR_WAIT)
  return cursor_pos


def initialize():
  pass

def shutdown():
  pass

