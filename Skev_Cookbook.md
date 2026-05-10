<!--
Copyright © 2026 AJ. All Rights Reserved.
skev.dev | skev.org
-->

# Skev Cookbook
## Common Game Patterns — Ready to Use
**Version:** 1.0 | Every example runs through the Python transpiler.

---

## A — Entity Patterns

### A1. Health System

```swift
kind DamageType >> physical  fire  ice << DamageType

data DamageEvent >>
    amount   :: float
    type_tag :: DamageType
    is_crit  :: bool
<< DamageEvent

entity HealthComponent >>
    health     :: int   = 100
    max_health :: int   = 100
    alive      :: bool  = true
    armour     :: int   = 10

    take_damage(event: DamageEvent) -> nothing
        effective :: float = event.amount - armour
        if effective < 1 >>
            effective = 1.0
        << effective < 1
        if event.is_crit >>
            effective = effective * 2.0
        << event.is_crit
        health = math.clamp(health - effective, 0, max_health)
        if health <= 0 >>
            alive = false
        << health <= 0
    << take_damage

    heal(amount: int) -> nothing
        if alive >>
            health = math.clamp(health + amount, 0, max_health)
        << alive
    << heal

    percent() -> float
        result math.clamp(health / max_health, 0.0, 1.0)
    << percent

<< HealthComponent
// 33 lines total
```

---

### A2. Timer and Countdown

```swift
entity Timer >>
    duration    :: float
    elapsed     :: float = 0.0
    running     :: bool  = false
    finished    :: bool  = false

    start(duration_seconds: float) -> nothing
        duration = duration_seconds
        elapsed  = 0.0
        running  = true
        finished = false
    << start

    when update(delta)
        if running >>
            elapsed += delta
            if elapsed >= duration >>
                elapsed  = duration
                running  = false
                finished = true
            << elapsed >= duration
        << running
    << update

    remaining() -> float
        result math.clamp(duration - elapsed, 0.0, duration)
    << remaining

    progress() -> float
        if duration <= 0 >>
            result 1.0
        << duration <= 0
        result math.clamp(elapsed / duration, 0.0, 1.0)
    << progress

<< Timer
// 33 lines total — start(5.0) runs a 5-second countdown
```

---

### A3. State Machine

```swift
kind PlayerState >>
    idle
    running
    jumping
    falling
    dead
<< PlayerState

entity StateMachine >>
    state        :: PlayerState = PlayerState.idle
    prev_state   :: PlayerState = PlayerState.idle
    state_time   :: float       = 0.0

    transition(new_state: PlayerState) -> bool
        if state == new_state >>
            result false
        << state == new_state
        prev_state = state
        state      = new_state
        state_time = 0.0
        result true
    << transition

    when update(delta)
        state_time += delta
    << update

    is_in(check: PlayerState) -> bool
        result state == check
    << is_in

    came_from(check: PlayerState) -> bool
        result prev_state == check
    << came_from

<< StateMachine
// 32 lines total
```

---

### A4. Object Pool

```swift
data PooledBullet >>
    position :: Vector3!
    velocity :: Vector3!
    lifetime :: float
    active   :: bool = false
<< PooledBullet

entity BulletPool >>
    pool     :: list[PooledBullet]
    pool_size :: int = 64

    when scene_load
        loop i from 0 to pool_size >>
            pool.append(PooledBullet(
                position = Vector3(0.0, 0.0, 0.0),
                velocity = Vector3(0.0, 0.0, 0.0),
                lifetime = 0.0,
                active   = false
            ))
        << i
    << scene_load

    spawn(pos: Vector3!, vel: Vector3!, life: float) -> bool
        loop bullet in pool >>
            if not bullet.active >>
                bullet.position = pos
                bullet.velocity = vel
                bullet.lifetime = life
                bullet.active   = true
                result true
            << not bullet.active
        << bullet
        result false
    << spawn

    when update(delta)
        loop bullet in pool >>
            if bullet.active >>
                bullet.position += bullet.velocity * delta
                bullet.lifetime -= delta
                if bullet.lifetime <= 0 >>
                    bullet.active = false
                << bullet.lifetime <= 0
            << bullet.active
        << bullet
    << update

<< BulletPool
// 44 lines total — 64 bullets, zero allocation after scene_load
```

---

## B — Error Handling Patterns

### B1. Multi-Step Validation

```swift
kind ValidationError >>
    empty_name
    name_too_long
    negative_score
    invalid_level
<< ValidationError

data PlayerRecord >>
    name  :: string
    score :: int
    level :: int
<< PlayerRecord

entity Validator >>
    validate(record: PlayerRecord) -> result[PlayerRecord]
        step1 :: result[PlayerRecord] = validate_name(record)
        if step1.is_failure >>
            fail step1.error
        << step1.is_failure

        step2 :: result[PlayerRecord] = validate_score(step1.value)
        if step2.is_failure >>
            fail step2.error
        << step2.is_failure

        succeed step2.value
    << validate

    validate_name(r: PlayerRecord) -> result[PlayerRecord]
        if r.name == "" >>
            fail ValidationError.empty_name
        << r.name == ""
        if r.name.__len__() > 20 >>
            fail ValidationError.name_too_long
        << r.name.__len__() > 20
        succeed r
    << validate_name

    validate_score(r: PlayerRecord) -> result[PlayerRecord]
        if r.score < 0 >>
            fail ValidationError.negative_score
        << r.score < 0
        succeed r
    << validate_score

<< Validator
// 43 lines total
```

---

### B2. Save and Load

```swift
entity SaveSystem >>
    save_path :: string = "save/player.json"

    save(name: string, score: int, level: int) -> result[nothing]
        data_str :: string = "{\"name\":\"{name}\",\"score\":{score},\"level\":{level}}"
        result_write :: result[nothing] = file.write_text(save_path, data_str)
        if result_write.is_failure >>
            fail result_write.error
        << result_write.is_failure
        succeed nothing
    << save

    load() -> result[string]
        r :: result[string] = file.read_text(save_path)
        if r.is_failure >>
            fail r.error
        << r.is_failure
        if not json.is_valid(r.value) >>
            fail file.FileError.read_error
        << not json.is_valid(r.value)
        succeed r.value
    << load

    has_save() -> bool
        result file.exists(save_path)
    << has_save

    delete_save() -> result[nothing]
        result file.delete_file(save_path)
    << delete_save

<< SaveSystem
// 33 lines total
```

---

## C — Concurrency Patterns

### C1. Background Loading

```swift
data LoadResult >>
    asset_name :: string
    success    :: bool
    error_msg  :: string
<< LoadResult

entity AssetLoader >>
    load_channel :: channel[LoadResult]
    loaded_count :: int = 0

    load_async(asset_name: string) -> nothing
        task load_asset >>
            # Simulate load — replace with real file.read_text
            result :: result[string] = file.read_text(asset_name)
            if result.is_success >>
                load_channel.send(LoadResult(
                    asset_name = asset_name,
                    success    = true,
                    error_msg  = ""
                ))
            << result.is_success
            else >>
                load_channel.send(LoadResult(
                    asset_name = asset_name,
                    success    = false,
                    error_msg  = "Failed to load"
                ))
            << else
        << task
    << load_async

    when update(delta)
        loop while load_channel.has_message >>
            result :: LoadResult = load_channel.receive()
            if result.success >>
                loaded_count += 1
            << result.success
        << while load_channel.has_message
    << update

<< AssetLoader
// 38 lines total — loads assets without blocking the game loop
```

---

## D — Game-Specific Patterns

### D1. Camera Follow with Smoothing

```swift
entity Camera >>
    position   :: Vector3!
    target_pos :: Vector3!
    follow_speed :: float = 5.0
    look_ahead :: float   = 2.0

    follow(target: Vector3!, velocity: Vector3!) -> nothing
        # Look ahead based on movement direction
        ahead :: Vector3! = Vector3(
            target.x + velocity.x * look_ahead,
            target.y + velocity.y * look_ahead,
            target.z + velocity.z * look_ahead
        )
        target_pos = ahead
    << follow

    when update(delta)
        # Smooth follow using lerp
        position = Vector3(
            math.lerp(position.x, target_pos.x, follow_speed * delta),
            math.lerp(position.y, target_pos.y, follow_speed * delta),
            math.lerp(position.z, target_pos.z, follow_speed * delta)
        )
    << update

<< Camera
// 26 lines total
```

---

### D2. Score System with Multiplier

```swift
entity ScoreSystem >>
    score        :: int = 0
    high_score   :: int = 0
    multiplier   :: int = 1
    combo_count  :: int = 0
    combo_timer  :: float = 0.0
    combo_window :: float = 2.0

    add_score(base_points: int) -> int
        earned :: int = base_points * multiplier
        score += earned
        if score > high_score >>
            high_score = score
        << score > high_score
        combo_count += 1
        combo_timer  = combo_window
        multiplier   = math.clamp_int(combo_count, 1, 8)
        result earned
    << add_score

    when update(delta)
        if combo_timer > 0 >>
            combo_timer -= delta
            if combo_timer <= 0 >>
                combo_count = 0
                multiplier  = 1
            << combo_timer <= 0
        << combo_timer > 0
    << update

    reset() -> nothing
        score       = 0
        multiplier  = 1
        combo_count = 0
        combo_timer = 0.0
    << reset

<< ScoreSystem
// 38 lines total
```

---

### D3. Terrain Noise Generator

```swift
data TerrainChunk >>
    x      :: int
    z      :: int
    width  :: int
    height :: int
<< TerrainChunk

entity TerrainGenerator >>
    scale      :: float = 0.01
    amplitude  :: float = 50.0
    octaves    :: int   = 4

    sample_height(world_x: float, world_z: float) -> float
        h      :: float = 0.0
        amp    :: float = amplitude
        freq   :: float = scale
        loop i from 0 to octaves >>
            h   += math.noise2(world_x * freq, world_z * freq) * amp
            amp  = amp * 0.5
            freq = freq * 2.0
        << i
        result h
    << sample_height

    is_water(world_x: float, world_z: float) -> bool
        result sample_height(world_x, world_z) < 0.0
    << is_water

    is_mountain(world_x: float, world_z: float) -> bool
        result sample_height(world_x, world_z) > amplitude * 0.6
    << is_mountain

<< TerrainGenerator
// 32 lines total
```

---

### D4. UFO Beam System (Road Fighter Pattern)

```swift
kind BeamPhase >>
    inactive
    warning
    firing
    retracting
<< BeamPhase

entity UFOBeamSystem >>
    phase          :: BeamPhase = BeamPhase.inactive
    phase_timer    :: float = 0.0
    warning_dur    :: float = 0.5
    fire_dur       :: float = 1.5
    retract_dur    :: float = 0.3
    shadow_scale   :: float = 0.0
    beam_channel   :: channel[bool]

    fire_beam() -> bool
        if phase != BeamPhase.inactive >>
            result false
        << phase != BeamPhase.inactive
        phase       = BeamPhase.warning
        phase_timer = warning_dur
        shadow_scale = 1.0
        result true
    << fire_beam

    when update(delta)
        if phase == BeamPhase.inactive >>
            result nothing
        << phase == BeamPhase.inactive

        phase_timer -= delta

        if phase == BeamPhase.warning >>
            # Shadow shrinks to show warning
            shadow_scale = math.clamp(phase_timer / warning_dur, 0.0, 1.0)
            if phase_timer <= 0 >>
                phase       = BeamPhase.firing
                phase_timer = fire_dur
                beam_channel.send(true)
            << phase_timer <= 0
        << phase == BeamPhase.warning

        if phase == BeamPhase.firing >>
            if phase_timer <= 0 >>
                phase       = BeamPhase.retracting
                phase_timer = retract_dur
                beam_channel.send(false)
            << phase_timer <= 0
        << phase == BeamPhase.firing

        if phase == BeamPhase.retracting >>
            if phase_timer <= 0 >>
                phase        = BeamPhase.inactive
                shadow_scale = 0.0
            << phase_timer <= 0
        << phase == BeamPhase.retracting
    << update

<< UFOBeamSystem
// 52 lines total — the Road Fighter beam with warning shadow
```

---

### D5. Leaderboard with Backend

```swift
data LeaderboardEntry >>
    player_name :: string
    score       :: int
    rank        :: int
<< LeaderboardEntry

entity Leaderboard >>
    entries      :: list[LeaderboardEntry]
    api_url      :: string = "https://your-project.supabase.co/rest/v1/scores"
    api_key      :: string = ""
    loading      :: bool   = false
    fetch_channel :: channel[string]

    fetch_async() -> nothing
        if loading >>
            result nothing
        << loading
        loading = true
        task fetch >>
            response :: result[HttpResponse] = network.http_get_headers(
                api_url, api_key
            )
            if response.is_success >>
                fetch_channel.send(response.value.body)
            << response.is_success
            else >>
                fetch_channel.send("")
            << else
        << task
    << fetch_async

    when update(delta)
        loop while fetch_channel.has_message >>
            raw :: string = fetch_channel.receive()
            loading = false
            if raw != "" >>
                parse_entries(raw)
            << raw != ""
        << while fetch_channel.has_message
    << update

    submit(player_name: string, score: int) -> result[nothing]
        body :: string = "{\"name\":\"{player_name}\",\"score\":{score}}"
        r :: result[HttpResponse] = network.http_post(api_url, body, api_key)
        if r.is_failure >>
            fail r.error
        << r.is_failure
        if not r.value.ok >>
            fail network.NetworkError.server_error
        << not r.value.ok
        succeed nothing
    << submit

    parse_entries(raw: string) -> nothing
        if not json.is_valid(raw) >>
            result nothing
        << not json.is_valid(raw)
        entries.clear()
    << parse_entries

<< Leaderboard
// 58 lines total — async fetch, non-blocking, real Supabase pattern
```

---

## E — Utility Patterns

### E1. Achievement Tracker

```swift
kind AchievementStatus >> locked  unlocked << AchievementStatus

data Achievement >>
    id        :: int
    name      :: string
    threshold :: int
    status    :: AchievementStatus = AchievementStatus.locked
    progress  :: int = 0
<< Achievement

entity AchievementSystem >>
    achievements   :: list[Achievement]
    total_unlocked :: int = 0

    add(id: int, name: string, threshold: int) -> nothing
        achievements.append(Achievement(
            id        = id,
            name      = name,
            threshold = threshold
        ))
    << add

    progress(ach_id: int, amount: int) -> bool
        loop ach in achievements >>
            if ach.id == ach_id >>
                ach.progress += amount
                if ach.progress >= ach.threshold >>
                    if ach.status == AchievementStatus.locked >>
                        ach.status = AchievementStatus.unlocked
                        total_unlocked += 1
                        result true
                    << ach.status == AchievementStatus.locked
                << ach.progress >= ach.threshold
                result false
            << ach.id == ach_id
        << ach
        result false
    << progress

    is_unlocked(ach_id: int) -> bool
        loop ach in achievements >>
            if ach.id == ach_id >>
                result ach.status == AchievementStatus.unlocked
            << ach.id == ach_id
        << ach
        result false
    << is_unlocked

<< AchievementSystem
// 44 lines total
```

---

*Copyright © 2026 AJ. All Rights Reserved. skev.dev | skev.org*
