def compute_load_schedule(pattern, qps, duration, concurrency, spike_duration=None, spike_load=None, spike_interval=None):
    if pattern == "steady":
        return [qps] * duration
    elif pattern == "spike":
        normal_duration = (duration - spike_duration) // 2
        spike_load_schedule = [qps] * normal_duration + [spike_load] * spike_duration + [qps] * normal_duration
        return spike_load_schedule[:duration]
    elif pattern == "periodic":
        load = []
        while len(load) < duration:
            load += [qps] * (spike_interval - spike_duration) + [spike_load] * spike_duration
        return load[:duration]
    else:
        raise ValueError("Unsupported load pattern")