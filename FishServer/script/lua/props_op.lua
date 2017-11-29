local function to_number(val, dft)
    local v = tonumber(val)
    if v == nil then
        v = dft
    end
    return v
end

local function get_props(uid, gid, pid)
    local key = 'props:' .. gid .. ':' .. uid
    local data = redis.call('hget', key, pid)
    return to_number(data, 0)
end

local function incr_props(uid, gid, pid, count)
    local key = 'props:' .. gid .. ':' .. uid
    local data = redis.call('hget', key, pid)
    data = to_number(data, 0)
    local fix = 0
    if data < 0 then
        fix = -data
        data = 0
        redis.call('hset', key, pid, 0)
    end
    local left = data + count
    if left == 0 then
        redis.call('hdel', key, pid)
        return { count, left, fix }
    elseif left > 0 then
        redis.call('hset', key, pid, left)
        return { count, left, fix }
    else
        return { 0, 0, fix }
    end
end

local function mincr_props(KEYS)
    local uid, gid = KEYS[2], KEYS[3]
    local key = 'props:' .. gid .. ':' .. uid
    local total = #KEYS
    if total < 5 or total % 2 == 0 then
        return redis.error_reply('error count')
    end
    local check_keys, check_values = {}, {}
    for i = 4, total, 2 do
        KEYS[i + 1] = tonumber(KEYS[i + 1])
        if KEYS[i + 1] == nil then
            return redis.error_reply('error param ' .. tostring(i + 1))
        end
        if KEYS[i + 1] < 0 then
            table.insert(check_keys, KEYS[i])
            table.insert(check_values, KEYS[i + 1])
        end
    end
    if #check_keys > 0 then
        local vars = redis.call('HMGET', key, unpack(check_keys))
        for i = 1, #vars, 1 do
            if to_number(vars[i], 0) + check_values[i] < 0 then
                return {1, 'lack ' .. check_keys[i]}
            end
        end
    end
    local results = {}
    for i = 4, total, 2 do
        local final = redis.call('HINCRBY', key, KEYS[i], KEYS[i + 1])
        table.insert(results, final)
    end
    return {0, results}
end

local action = KEYS[1]
if action == 'get' then
    return get_props(KEYS[2], KEYS[3], KEYS[4])
elseif action == 'incr' then
    return incr_props(KEYS[2], KEYS[3], KEYS[4], tonumber(KEYS[5]))
elseif action == 'mincr' then
    return mincr_props(KEYS)
end
