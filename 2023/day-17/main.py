from heapq import heappush, heappop

# read from stdin, quicker
grid = [[int(x) for x in line.strip()] for line in open(0)]

seen = set()

pq: list[tuple[int, int, int, int, int, int]] = [(0, 0, 0, 0, 0, 0)]

while pq:
    # heat loss, row, column, direction row, direction col, n steps same dir
    hl, r, c, dr, dc, n = heappop(pq)

    if r == len(grid) - 1 and c == len(grid[0]) - 1:
        print(hl)
        break

    if (r, c, dr, dc, n) in seen:
        continue

    seen.add((r, c, dr, dc, n))

    if n < 3 and (dr, dc) != (0, 0):
        nr = r + dr
        nc = c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            heappush(pq, (hl + grid[nr][nc], nr, nc, dr, dc, n + 1))

    for ndr, ndc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        if (ndr, ndc) != (dr, dc) and (ndr, ndc) != (-dr, -dc):
            nr = r + ndr
            nc = c + ndc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                heappush(pq, (hl + grid[nr][nc], nr, nc, ndr, ndc, 1))

pq = [(0, 0, 0, 0, 0, 0)]
seen = set()

while pq:
    hl, r, c, dr, dc, n = heappop(pq)

    if r == len(grid) - 1 and c == len(grid[0]) - 1 and n >= 4:
        print(hl)
        break

    if (r, c, dr, dc, n) in seen:
        continue

    seen.add((r, c, dr, dc, n))

    if n < 10 and (dr, dc) != (0, 0):
        nr = r + dr
        nc = c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            heappush(pq, (hl + grid[nr][nc], nr, nc, dr, dc, n + 1))

    if n >= 4 or (dr, dc) == (0, 0):
        for ndr, ndc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if (ndr, ndc) != (dr, dc) and (ndr, ndc) != (-dr, -dc):
                nr = r + ndr
                nc = c + ndc
                if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                    heappush(pq, (hl + grid[nr][nc], nr, nc, ndr, ndc, 1))
