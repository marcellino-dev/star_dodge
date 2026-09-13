import pygame
import pytest

from project import (
    check_collision,
    clamp,
    load_highscore,
    save_highscore,
    spawn_obstacle,
    update_obstacles,
)


def test_clamp():
    assert clamp(5, 0, 10) == 5
    assert clamp(-5, 0, 10) == 0
    assert clamp(15, 0, 10) == 10


def test_spawn_obstacle():
    obstacles = []
    spawn_obstacle(obstacles, difficulty=0)
    assert len(obstacles) == 1
    obstacle = obstacles[0]
    assert obstacle["y"] < 0
    assert obstacle["radius"] > 0
    assert obstacle["speed"] > 0


def test_update_obstacles_moves_and_removes():
    obstacles = [{"x": 100, "y": 620, "radius": 10, "speed": 5}]
    updated = update_obstacles(obstacles)
    assert len(updated) == 0

    obstacles = [{"x": 100, "y": 100, "radius": 10, "speed": 5}]
    updated = update_obstacles(obstacles)
    assert len(updated) == 1
    assert updated[0]["y"] == 105


def test_check_collision_detects_overlap():
    player = pygame.Rect(100, 100, 40, 40)
    obstacles = [{"x": 120, "y": 120, "radius": 15, "speed": 3}]
    hit = check_collision(player, obstacles)
    assert hit is not None


def test_check_collision_no_overlap():
    player = pygame.Rect(0, 0, 40, 40)
    obstacles = [{"x": 700, "y": 500, "radius": 15, "speed": 3}]
    hit = check_collision(player, obstacles)
    assert hit is None


def test_save_and_load_highscore(tmp_path):
    path = tmp_path / "highscore.txt"
    assert load_highscore(path) == 0

    result = save_highscore(path, 50)
    assert result == 50
    assert load_highscore(path) == 50

    result = save_highscore(path, 20)
    assert result == 50
    assert load_highscore(path) == 50


if __name__ == "__main__":
    pytest.main([__file__, "-v"])