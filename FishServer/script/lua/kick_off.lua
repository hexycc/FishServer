-- KEYS: [userId, gameId, total, [tableId]]
-- ARGV: []
--  ACK: [seatid, before_cnt, after_cnt]

local function to_number(val, dft)
    local v = tonumber(val)
    if v == nil then
        v = dft
    end
    return v
end

local function get_attrs(total)
    local attrs = {}
    for i = 1, total do
        table.insert(attrs, 'seat'..tostring(i-1))
    end
    return attrs
end

local function get_player_count(key, total)
    local attrs = get_attrs(total)

    local res = redis.call('HMGET', key, unpack(attrs))
    local cnt = 0
    for i = 1, total do
        if res[i] and tonumber(res[i]) > 0 then
            cnt = cnt + 1
        end
    end
    return cnt
end

local function leave_table(uid, key, total)
    local attrs = get_attrs(total)
    local res = redis.call('HMGET', key, unpack(attrs))
    local sid = -1
    for i = 1, total do
        if res[i] == uid then
            sid = i - 1
            local field = 'seat' .. tostring(sid)
            redis.call('HSET', key, field, 0)
        end
    end
    return sid
end

local function get_user_location(uid, gid)
    local key = 'location:' .. gid .. ':' .. uid
    local res = redis.call('HMGET', key, 'room_type', 'table_id', 'play_mode')
    redis.call('DEL', key)
    if not res[1] or not res[2] then
        return -1, -1, res[3]
    end
    return tonumber(res[1]), tonumber(res[2]), tonumber(res[3])
end

local function kick_off(uid, gid, total, tid)
    local rid, _tid, mode = get_user_location(uid, gid)

    if rid < 0 or _tid < 0 then
        repeat
            _tid = tid
            if _tid > 0 then
                local rid_mode = redis.call('HMGET', 'table:' .. gid .. ':' .. tostring(_tid), 'room_type', 'play_mode')
                rid, mode = rid_mode[1], rid_mode[2]
                if rid then
                    rid = tonumber(rid)
                    break
                end
            end
            return { -1, -1, -1 }
        until true
    end

    local key = 'table:' .. gid .. ':' .. tostring(_tid)
    local before_cnt = get_player_count(key, total)
    local sid = leave_table(uid, key, total)

    local before_key = 'quick:' .. gid .. ':0'
    if before_cnt ~= 0 then
        if mode ~= nil then
            before_key = 'quick:' .. gid .. ':' .. tostring(rid) .. ':' .. tostring(before_cnt) .. ':' .. mode
        else
            before_key = 'quick:' .. gid .. ':' .. tostring(rid) .. ':' .. tostring(before_cnt)
        end
    end

    local after_cnt = get_player_count(key, total)
    local after_key = 'quick:' .. gid .. ':0'
    if after_cnt ~= 0 then
        if mode ~= nil then
            after_key = 'quick:' .. gid .. ':' .. tostring(rid) .. ':' .. tostring(after_cnt) .. ':' .. mode
        else
            after_key = 'quick:' .. gid .. ':' .. tostring(rid) .. ':' .. tostring(after_cnt)
        end
    end

    if before_cnt ~= after_cnt then
        redis.call('LREM', before_key, '0', _tid)
        redis.call('RPUSH', after_key, _tid)
    end
    if after_cnt == 0 then
        local res = redis.call('HMGET', key, 'area', 'table', 'play_mode')
        if res[1] and res[2] then
            local area_key = 'area:' .. gid .. ':' .. tostring(res[1])
            redis.call('HDEL', area_key, res[2])
        end
    end

    return { sid, before_cnt, after_cnt }
end

local total = tonumber(KEYS[3])
local tid = to_number(KEYS[4], 0)
return kick_off(KEYS[1], KEYS[2], total, tid)
