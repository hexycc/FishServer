#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-01-07

from framework.helper import *

product_100632 = {
    'price': 12,
    'name': u'12元捕鱼金币礼包',
    'desc': {
        'display': u'加赠5%',
        'addition': 3600,
        'amount': 72000
    },
    'content': {
        'chip': 75600
    },
    'first': {
        'chip': 144000
    }
}

product_100633 = {
    'price': 28,
    'name': u'28元捕鱼金币礼包',
    'desc': {
        'display': u'加赠10%',
        'addition': 16800,
        'amount': 168000
    },
    'content': {
        'chip': 184800
    },
    'first': {
        'chip': 336000
    }
}

product_100634 = {
    'price': 50,
    'name': u'50元捕鱼金币礼包',
    'desc': {
        'display': u'加赠15%',
        'addition': 45000,
        'amount': 300000
    },
    'content': {
        'chip': 345000
    },
    'first': {
        'chip': 600000
    }
}

product_100635 = {
    'price': 108,
    'name': u'108元捕鱼金币礼包',
    'desc': {
        'display': u'加赠20%',
        'addition': 129600,
        'amount': 648000
    },
    'content': {
        'chip': 777600
    },
    'first': {
        'chip': 1296000
    }
}

product_100636 = {
    'price': 328,
    'name': u'328元捕鱼金币礼包',
    'desc': {
        'display': u'加赠25%',
        'addition': 492000,
        'amount': 1968000
    },
    'content': {
        'chip': 2460000
    },
    'first': {
        'chip': 3936000
    }
}

product_100637 = {
    'price': 618,
    'name': u'618元捕鱼金币礼包',
    'desc': {
        'display': u'加赠30%',
        'addition': 1124000,
        'amount': 3708000
    },
    'content': {
        'chip': 4820400
    },
    'first': {
        'chip': 7416000
    }
}

product_100638 = {
    'price': 12,
    'name': u'12元捕鱼钻石礼包',
    'desc': {
        'amount': 120
    },
    'content': {
        'diamond': 120
    }
}

product_100639 = {
    'price': 28,
    'name': u'28元捕鱼钻石礼包',
    'desc': {
        'display': u'加赠10%',
        'addition': 28,
        'amount': 280
    },
    'content': {
        'diamond': 308
    }
}

product_100640 = {
    'price': 50,
    'name': u'50元捕鱼钻石礼包',
    'desc': {
        'display': u'加赠15%',
        'addition': 75,
        'amount': 500
    },
    'content': {
        'diamond': 575
    }
}

product_100641 = {
    'price': 108,
    'name': u'108元捕鱼钻石礼包',
    'desc': {
        'display': u'加赠20%',
        'addition': 216,
        'amount': 1080
    },
    'content': {
        'diamond': 1296
    }
}

product_100642 = {
    'price': 328,
    'name': u'328元捕鱼钻石礼包',
    'desc': {
        'display': u'加赠25%',
        'addition': 820,
        'amount': 3280
    },
    'content': {
        'diamond': 4100
    }
}

month_card_reward = {
    'chip': 20000,
    'diamond': 20,
    'props': [{'id': 201, 'count': 5}, {'id': 202, 'count': 2}],
}

add_game_config(2, 'month.card.reward', month_card_reward)

product_100630 = {
    'price': 28,
    'name': u'贵族礼包',
    'content': month_card_reward
}

product_100631 = {
    'price': 1,
    'name': u'首充礼包',
    'worth': 18,
    'content': {
        'diamond': 100,
        'chip': 10000,
        'props': [{'id': 201, 'count': 5}, {'id': 202, 'count': 5}],
    }
}

product_100668 = {
    'price': 6,
    'name': u'首充礼包',
    'worth': 38,
    'content': {
        'diamond': 100,
        'chip': 100000,
        'props': [{'id': 201, 'count': 10}, {'id': 202, 'count': 10}]
    }
}

__product_config = {
    '100632': product_100632,
    '100633': product_100633,
    '100634': product_100634,
    '100635': product_100635,
    '100636': product_100636,
    '100637': product_100637,
    '100638': product_100638,
    '100639': product_100639,
    '100640': product_100640,
    '100641': product_100641,
    '100642': product_100642,
    '100630': product_100630,
    '100631': product_100631,
    '100668': product_100668,
}

__shop_config = {
    'chip': ['100637', '100636', '100635', '100634', '100633', '100632'],
    'diamond': ['100642', '100641', '100640', '100639', '100638'],
    'card': ['100630'],
    'first': ['100631', '100668']
}

add_game_config(2, 'product.config', __product_config)

add_game_config(2, 'shop.config', __shop_config)

add_game_config(2, 'jiyu.app.info', {
    'appId': '11116',
    'appKey': 'd9715c51711126fa78012121541f6961b30136f038e',
})
