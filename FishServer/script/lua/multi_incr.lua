-- KEYS: [op, key, field, delta, [field, delta...]]
-- ARGV: []
--  ACK: [final, [...]]

local function is_not_number(num)
    local n = tonumber(num)
    return n == nil
end

local function hash_multi_incr(KEYS)
    local total = #KEYS
    if total < 4 or total % 2 == 1 then
        return redis.error_reply('error count')
    end
    for i = 3, total, 2 do
        if is_not_number(KEYS[i + 1]) then
            return redis.error_reply('error param ' .. tostring(i + 1))
        end
    end
    local key, results = KEYS[2], {}
    for i = 3, total, 2 do
        local final = redis.call('HINCRBY', key, KEYS[i], KEYS[i + 1])
        table.insert(results, final)
    end
    return results
end

local function multi_incr(KEYS)
    local total = #KEYS
    if total < 3 or total % 2 == 0 then
        return redis.error_reply('error count')
    end
    for i = 2, total, 2 do
        if is_not_number(KEYS[i + 1]) then
            return redis.error_reply('error param ' .. tostring(i + 1))
        end
    end
    local results = {}
    for i = 2, total, 2 do
        local final = redis.call('INCRBY', KEYS[i], KEYS[i + 1])
        table.insert(results, final)
    end
    return results
end

local op = tonumber(KEYS[1])
if op == 1 then
    return multi_incr(KEYS)
elseif op == 2 then
    return hash_multi_incr(KEYS)
else
    return redis.error_reply('error op')
end
