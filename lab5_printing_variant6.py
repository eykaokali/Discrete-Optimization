from typing import List, Dict
from dataclasses import dataclass
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int
    min_items: int = 1


def _to_jobs(print_jobs: List[Dict]) -> List[PrintJob]:
    return [PrintJob(**job) for job in print_jobs]


def _to_constraints(constraints: Dict) -> PrinterConstraints:
    return PrinterConstraints(
        max_volume=constraints["max_volume"],
        max_items=constraints["max_items"],
        min_items=constraints.get("min_items", 1),
    )


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    jobs = _to_jobs(print_jobs)
    cons = _to_constraints(constraints)

    if cons.min_items < 1:
        raise ValueError("min_items має бути >= 1")
    if cons.max_items < 1:
        raise ValueError("max_items має бути >= 1")

    remaining = sorted(jobs, key=lambda j: (j.priority, j.id))

    print_order: List[str] = []
    total_time = 0

    while remaining:
        batch: List[PrintJob] = []
        batch_volume = 0.0

        i = 0
        while i < len(remaining):
            job = remaining[i]
            can_add = (
                len(batch) < cons.max_items
                and batch_volume + job.volume <= cons.max_volume
            )
            if can_add:
                batch.append(job)
                batch_volume += job.volume
                remaining.pop(i)
            else:
                i += 1

            if len(batch) >= cons.max_items:
                break

        if not batch and remaining:
            job = remaining.pop(0)
            batch = [job]
            batch_volume = job.volume

        for job in batch:
            print_order.append(job.id)

        batch_time = max(j.print_time for j in batch)
        total_time += batch_time

    return {
        "print_order": print_order,
        "total_time": total_time,
    }


def test_printing_optimization():
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150},
    ]

    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150},
    ]

    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120},
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2,
        "min_items": 2,
    }

    print("=" * 60)
    print("| Завдання 2 | 3D-друк | Варіант 6")
    print(f"Обмеження: {constraints}")
    print("=" * 60)

    print("\nТест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")

    assert result1["print_order"] == ["M1", "M2", "M3"]
    assert result1["total_time"] == 270
    assert result2["print_order"] == ["M2", "M1", "M3"]
    assert result2["total_time"] == 270
    assert result3["print_order"] == ["M1", "M2", "M3"]
    assert result3["total_time"] == 450
    print("\nУсі тести пройшли успішно!")


if __name__ == "__main__":
    test_printing_optimization()
