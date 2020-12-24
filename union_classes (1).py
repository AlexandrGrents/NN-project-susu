import json
import os

def union_classes_in_dataset(dataset_dir, json_filename):

	with open(os.path.join(dataset_dir, json_filename), 'r') as f:
		data = json.load(f)

	print(data.keys())
	categories = data['categories']
	new_categories = []
	convert = {'minibus': 'bus', 'middle_bus':'bus','trolleybus':'bus', 'middle_truck': 'truck', 'van': 'truck', 'ambulance':'truck', 'tractor':'truck', 'fire_truck':'truck'}

	for_delete = ['tram', 'person', 'uncategorized']
	name_for_id = {}

	old_statistic = {}
	new_statistic = {}

	convert_category_id = {}
	delete_category_id = []

	category_id = 1
	for category in categories:
		if category['name'] in convert.keys() or category['name'] in for_delete:
			continue
		new_category = category.copy()
		new_category['id'] = category_id

		name_for_id[new_category['name']] = new_category['id']
		category_id+=1
		new_categories.append(new_category)


	for category in categories: 
		print(category)
		old_statistic[category['id']] = 0

	print('-'*20)

	for category in new_categories: 
		print(category)
		new_statistic[category['id']] = 0

	for category in categories:
		convert_category_name = convert.get(category['name'])
		if category['name'] in for_delete:
			delete_category_id.append(category['id'])
		elif convert_category_name:
			convert_category_id[category['id']] = name_for_id[convert_category_name]
		else:
			convert_category_id[category['id']] = name_for_id[category['name']]

	print('-'*20)

	print(convert_category_id)

	new_data = {'images':data['images'], 'categories':new_categories, 'annotations':[]}

	print(data['annotations'][0].keys())

	for annotation in data['annotations']:
		old_statistic[annotation['category_id']] +=1
		if annotation['category_id'] in delete_category_id:
			continue

		new_annotation = annotation.copy()

		new_annotation['category_id'] = convert_category_id[annotation['category_id']]
		new_data['annotations'].append(new_annotation.copy())

		
		new_statistic[new_annotation['category_id']] +=1

	print()
	print('OLD STATISTIC')
	total = 0
	for category_id, category_count in old_statistic.items():
		category_name = categories[category_id-1]['name']
		print(f'[{category_id}] {category_name} : {category_count}')
		total += category_count
	print('-'*20)
	print('total:', total)
	print('='*20)

	print('NEW STATISTIC')
	total = 0
	for category_id, category_count in new_statistic.items():
		category_name = new_categories[category_id-1]['name']
		print(f'[{category_id}] {category_name} : {category_count}')
		total += category_count
	print('-'*20)
	print('total:', total)
	print('='*20)



	with open (os.path.join(dataset_dir, 'union_classes.json'), 'w') as f:
		json.dump(new_data, f)

if __name__ == "__main__":
	union_classes_in_dataset('filtred_dataset', 'KomPol2-7.json')