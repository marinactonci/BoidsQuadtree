# BoidsQuadtree

BoidsQuadtree is a multiagent system simulation of flocking behavior, inspired by the Boids model developed by Craig Reynolds. It uses a Quadtree for efficient neighbor-finding, optimizing the simulation performance.

## Boids Multiagent System

The Boids model simulates the flocking behavior of birds. Each agent (a "boid") follows three simple rules - separation, alignment, and cohesion - which result in complex emergent behavior.

## Quadtree Optimization

A Quadtree is a tree data structure used to efficiently store data of points on a two-dimensional space. In this project, it's used to optimize the process of finding the neighboring boids for each individual boid, significantly reducing the computational complexity.

## Running the Project

Make sure you have Python installed on your machine and run the following commands:

```
$ git clone https://github.com/marinactonci/BoidsQuadtree.git
$ cd BoidQuadtree
$ python boids_quadtree.py
```
# BoidsQuadtree
