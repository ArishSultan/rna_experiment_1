from itertools import product


def _prop_groups(props):
    groups = []

    for prop in props:
        group = []

        if type(props[prop]) == list:
            for item in props[prop]:
                group.append({prop: item})
        else:
            group.append({prop: props[prop]})

        groups.append(group)

    return groups


def _flatten_prop_group(group):
    obj = dict()

    for item in group:
        key = list(item.keys())[0]
        obj[key] = item[key]

    return obj


def _should_ignore(obj, ignore_objs):
    for ignore_obj in ignore_objs:
        count = 0
        for key in ignore_obj:
            if key in obj and ignore_obj[key] == obj[key]:
                count += 1

        if count == len(ignore_obj):
            return True

    return False


def make_variant_name(name, encoding, props):
    prop_list = []
    prop_keys = sorted(list(props.keys()))

    for prop in prop_keys:
        prop_list.append(f'{prop}={props[prop]}')

    return f'{name}({encoding})[{";".join(prop_list)}]'


def prepare_variants(props, extra_props, ignore_combinations):
    valid_combos = []
    group_combos = product(*_prop_groups(props))

    for combo in group_combos:
        combo_obj = _flatten_prop_group(combo)

        if not _should_ignore(combo_obj, ignore_combinations):
            valid_combos.append((combo_obj, extra_props))

    return valid_combos
