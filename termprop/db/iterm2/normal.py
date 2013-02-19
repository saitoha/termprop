import re
combining_pattern=re.combile(u'/^[\u05e0-\u06bf\u08e6-\u08f3\u0b02-\u0b5b\u0b5e\u0b5f\u0b62-\u0b65\u0b68-\u0b6b\u0b6e\u0b6f\u0c00-\u0c15\u0c76-\u0c9f\u0cc0\u0cc1\u0d8c-\u0d99\u0d9e-\u0da9\u0dae-\u0db1\u0db4-\u0dbb\u0e02\u0e03\u0e40-\u0e75\u0f2c-\u0f41\u0fb6-\u0fc7\u100c-\u1013\u1016-\u1027\u102a-\u102f\u1032-\u103b\u1092-\u1097\u11e0-\u11e7\u1254-\u1259\u125c-\u127f\u1282-\u128f\u12a4-\u12a7\u12e2-\u12e7\u1358\u1359\u135c-\u1369\u136e-\u1371\u1376-\u137b\u138e\u138f\u13a4-\u13a7\u13e2-\u13e7\u1458\u1459\u145c-\u1465\u146e-\u1471\u1476-\u147b\u1482\u1483\u14c0-\u14c3\u14ca\u14cb\u14e2-\u14e7\u1558\u1559\u155c-\u156b\u156e-\u1573\u1576-\u157b\u15a4-\u15a7\u15e2-\u15e7\u1658\u1659\u165c-\u1669\u166e-\u1671\u1676-\u167b\u168c-\u168f\u16a4-\u16a7\u16e4\u16e5\u175c-\u1765\u176c-\u1771\u1774-\u177b\u178e\u178f\u17e2-\u17e7\u185c-\u1869\u186c-\u1871\u1874-\u187b\u188a-\u188d\u18a4-\u18a7\u18e4-\u18e7\u1958\u1959\u195c-\u1969\u196c-\u1971\u1974-\u197b\u198a-\u198d\u19a4-\u19a7\u19e4-\u19e7\u1a5c-\u1a69\u1a6c-\u1a71\u1a74-\u1a7b\u1a8e\u1a8f\u1aa4-\u1aa7\u1ae4-\u1ae7\u1b74\u1b75\u1b7e-\u1b89\u1b8c\u1b8d\u1b90-\u1b9f\u1bc4-\u1bc7\u1c42\u1c43\u1c48-\u1c55\u1c6e-\u1c7d\u1d42\u1d43\u1d48-\u1d53\u1d56-\u1d59\u1d70-\u1d7b\u1e10-\u1e13\u1e4a\u1e4b\u1e4e\u1e4f\u1e52\u1e53\u1e5c-\u1e5f\u1ec2-\u1ee9\u1eec-\u1eef\u1efa-\u1f0f\u1f12-\u1f59\u1f6c\u1f6d\u2036-\u205d\u208c-\u2093\u209c-\u20a1\u20a4-\u20a9\u20ae-\u20bb\u20c2-\u20c9\u20e4-\u20fb\u20fe\u20ff\u2114-\u211b\u269a-\u269f\u2e04-\u2e09\u2e44-\u2e49\u2e84-\u2e87\u2ec4-\u2ec7\u2f4c-\u2f87\u2f9a\u2f9b\u2ff6-\u2ffb\u3132\u3133\u3220-\u3237\u3240-\u3257\u3340-\u3361\u3370-\u3373\u340e-\u3417\u348a-\u349d\u34a0-\u34d9\u34de\u34df\u35e0-\u35e9\u3648-\u3669\u36b6-\u36c7\u36e0-\u36e5\u3722-\u3735\u37ac-\u37c7\u3828-\u384f\u3980-\u3985\u3988-\u39b1\u39ba\u39bb\u39c4\u39c5\u3b60-\u3bad\u3bd8-\u3bdf\u417d-\u41be\u59bb-\u59c0\u5adb\u5adc\u5b9d-\u5bdc\u6031-\u603c\u610f-\u6112\u14cbb-\u14cc2\u14cd5-\u14cd8\u14dbd-\u14dc0\u14fe1\u14fe2\u14fe9\u14fea\u14ff3\u14ff4\u15023-\u1502c\u150dd-\u150e0\u15145-\u15166\u1519d-\u151c0\u15229-\u15238\u1526b-\u15284\u152dd-\u152e4\u15343-\u1535e\u1542f-\u1544a\u15463\u15464\u15475-\u15478\u154d3\u154d4\u1553d\u1553e\u15541-\u15546\u1554b-\u1554e\u15559-\u1555c\u1555f\u15560\u157a3-\u157b2\u157b5-\u157b8\u1f619\u1f61a\u1fbdd-\u1fbfc\u1fc1d-\u1fc2a]$/')
fullwidth_pattern=re.combile(u'/^[\u21e0-\u229f\u2326-\u232f\u23d4-\u23df\u462f-\u4632\u5cdd-\u5d10\u5d13-\u5dc4\u5ddd-\u5f88\u5fbd-\u5fd4\u5fdd-\u6030\u603d-\u605a\u605f-\u610a\u6113-\u61dc\u61e7-\u6238\u623f-\u62fa\u62fd-\u6352\u635d-\u63a4\u63bd-\u641a\u641d-\u646c\u647d-\u65da\u65dd-\u9b5c\u9bdd-\u148f6\u148fd-\u1496a\u1529d-\u152d6\u157dd-\u1af24\u1af3d-\u1af6a\u1af73-\u1afd4\u1f1dd-\u1f5dc\u1fbfd-\u1fc10\u1fc3d-\u1fc82\u1fc85-\u1fcaa\u1fcad-\u1fcb4\u1fdde-\u1fe9d\u1ff9c-\u1ffa9]$/')
control_pattern=re.combile(u'/^[\u3ff6-\u3ff8\u1fddb]$/')