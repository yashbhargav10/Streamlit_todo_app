#Core Pkgs
import streamlit as st 

hide_st_style = """
			<style>
			#MainMenu {Visibility : hidden;}
			footer {Visibility: hidden;}
			header {Visibility: hidden;}
			</style>
			"""
st.markdown(hide_st_style, unsafe_allow_html = True)

#EDA PKGS
import pandas as pd
import plotly.express as px

#Database Functions
from db_fxn import (create_table, add_data, view_all_data, get_task, view_unique_tasks, edit_task_data, delete_data)

def main():
	
	st.title("To-Do APP with Streamlit")

	menu = ["Create", "Read", "Update", "Delete", "About"]
	choice = st.sidebar.selectbox("Menu", menu)

	create_table()
	if choice == "Create":
		st.subheader("Add Item")

		#Layouts
		col1, col2 = st.columns(2)

		with col1:
			task = st.text_area("Task To-Do")

		with col2:
			task_status = st.selectbox("Status", ["To-Do", "Doing", "Done"])
			task_due_date = st.date_input("Due Date")

		if st.button("Add Task"):
			add_data(task, task_status, task_due_date)
			st.success("Successfully Added Data : {}".format(task))



	elif choice == "Read":
		st.subheader("View Items")
		result = view_all_data()
		st.write(result)
		df = pd.DataFrame(result, columns = ['Task', 'Status', 'Due Date'])
		with st.expander("View All Data"):
			st.dataframe(df)

		with st.expander("Task Status"):
			task_df = df['Status'].value_counts().to_frame()
			
			task_df = task_df.reset_index()
			st.dataframe(task_df)

			p1 = px.pie(task_df, names = 'index', values = 'Status')
			st.plotly_chart(p1)

	elif choice == "Update":
		st.subheader("Edit/Update Items")
		result = view_all_data()
		df = pd.DataFrame(result, columns = ['Task', 'Status', 'Due Date'])
		with st.expander("Current Data"):
			st.dataframe(df)

		#st.write(view_unique_tasks())
		list_of_task = [i[0] for i in view_unique_tasks()]
		#st.write(list_of_task)

		selected_task = st.selectbox("Task to Edit", list_of_task)
		selected_result = get_task(selected_task)
		st.write(selected_result)
		if selected_result:
			task = selected_result[0][0]
			task_status = selected_result[0][1]
			task_due_date = selected_result[0][2]

			#Layouts
		col1, col2 = st.columns(2)

		with col1:
			new_task = st.text_area("Task To-Do", task)

		with col2:
			new_task_status = st.selectbox("Status", ["To-Do", "Doing", "Done"])
			new_task_due_date = st.date_input(task_due_date)

		if st.button("Update Task"):
			edit_task_data(new_task, new_task_status, new_task_due_date, task, task_status, task_due_date)
			st.success("Successfully Updated:: {} To ::{}".format(task, new_task))

		with st.expander("View Updated Data"):
				result = view_all_data()
				# st.write(result)
				clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
				st.dataframe(clean_df)




	elif choice == "Delete":
		st.subheader("Delete Item")
		result = view_all_data()
		df = pd.DataFrame(result, columns=['Task', 'Status', 'Due Date'])
		with st.expander("Current Data"):
			st.dataframe(df)

		list_of_task = [i[0] for i in view_unique_tasks()]
		selected_task = st.selectbox("Task To Edit", list_of_task)
		st.warning("Do you want to Delete ::{}".format(selected_task))
		if st.button("Delete Task"):
			delete_data(selected_task)
			st.success("Task has Successfully Deleted")

		with st.expander("View Updated Data"):
				result = view_all_data()
				# st.write(result)
				clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
				st.dataframe(clean_df)

	else:
		st.subheader("About")



if __name__ == '__main__':
	main()
