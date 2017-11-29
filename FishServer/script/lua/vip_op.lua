local function get_vip(uid, gid, today)
    local pid = 10
    local key = 'props:' .. gid .. ':' .. uid
    local _state, _left = 0, -1
    local data = redis.call('hget', key, pid)
    if data then
        local latest_day, left, state = unpack(cjson.decode(data))
        local expired_day = latest_day + left
        if expired_day >= today then
            _left = expired_day - today
            if latest_day == today then
                _state = state
            else
                _state = 0
            end
        end
    end

    return { _state, _left }
end

local function incr_vip(uid, gid, today, days)
    local pid = 10
    local key = 'props:' .. gid .. ':' .. uid
    local data = redis.call('hget', key, pid)
    local _state, _left = 0, days
    if data then
        local latest_day, left, state = unpack(cjson.decode(data))
        local expired_day = latest_day + left
        if expired_day >= today then
            _left = expired_day + days - today
            if latest_day == today then
                _state = state
            end
        end
    end
    data = cjson.encode({ today, _left, _state })
    redis.call('hset', key, pid, data)
    return { _state, _left }
end

local function use_vip(uid, gid, today)
    local pid = 10
    local key = 'props:' .. gid .. ':' .. uid
    local data = redis.call('hget', key, pid)
    if data then
        local latest_day, left, state = unpack(cjson.decode(data))
        local expired_day = latest_day + left
        -- expired
        if expired_day < today then
            redis.call('hdel', key, pid)
            return { 0, 0 }
        end
        local _left = expired_day - today
        -- already use
        if latest_day == today and state == 1 then
            return { 0, _left }
        end
        data = cjson.encode({ today, _left, 1 })
        redis.call('hset', key, pid, data)
        return { 1, _left }
    end
    return { 0, 0 }
end

local action = KEYS[1]
if action == 'get' then
    return get_vip(KEYS[2], KEYS[3], tonumber(KEYS[4]))
elseif action == 'incr' then
    return incr_vip(KEYS[2], KEYS[3], tonumber(KEYS[4]), tonumber(KEYS[5]))
elseif action == 'use' then
    return use_vip(KEYS[2], KEYS[3], tonumber(KEYS[4]))
end
