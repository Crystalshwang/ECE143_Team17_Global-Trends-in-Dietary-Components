'''
Group 17: Tao Liang, Ke Liu, Chenfeng Wu, Sihan Wang
Project name: Global trends in dietary components
Abstract: Analyze global food trends according to different countries and years
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyecharts
from pyecharts import Style
from pyecharts import Map, Geo
from pyecharts import Timeline
from pyecharts import Pie
from pyecharts_snapshot.main import make_a_snapshot

class Visualization:
    '''
    Create  Visualization object that contains all the data we need
    Define functions that can graph various plots
    '''
    def __init__(self):
        # set property of graphs
        self._color = 'firebrick'
        self._transparency = 0.85
        self._fontsize = 12
        
        # load all the data for visualization
        self.df_crops=None
        self.df_meats=None
        self.macronutrient = pd.read_csv('data/caloric-supply-from-carbohydrates-protein-and-fat.csv')
        self.foodGroup = pd.read_csv('data/dietary-compositions-by-commodity-group.csv')
        self.fruit = pd.read_csv('data/fruit-consumption-per-capita.csv')
        self.vegetable = pd.read_csv('data/vegetable-consumption-per-capita.csv')
        self.meat = pd.read_csv('data/FAOSTAT_data_3-10-2019.csv')
        self.diet = pd.read_csv('data/dietary-compositions-by-commodity-group.csv')
        self.food = pd.read_csv('data/global_food_consumption.csv')
        self.dataloader()
        
    def radarChart_for_macronutrient(self):
        '''
        Compute the mean of daily macronutrient intake 
        and plot a radar chart to represent the four nutrients
        '''
        df=self.macronutrient
        
        # labels
        name = ['Animal protein','Plant protein','Fat','Carbohydrates']   
        
        # divide the circle to uniform part
        theta = np.linspace(0,2*np.pi,len(name),endpoint=False)
        
        # mean kilocalories in different macronutrient
        value = [df[i].mean() for i in df.columns[3:]]
        theta = np.concatenate((theta,[theta[0]]))
        value = np.concatenate((value,[value[0]]))
        
        # graph the plot
        ax = plt.subplot(111,projection = 'polar')      
        ax.plot(theta,value,lw=1,alpha = 0.75,color=self._color)   
        ax.fill(theta,value,color='firebrick',alpha = self._transparency)       
        ax.set_thetagrids(theta*180/np.pi,name,fontsize=self._fontsize)        
        ax.set_ylim(0,2000)                                                     
        ax.set_theta_zero_location('S')                                         
        ax.set_title('daily caloric supply',fontsize = 15,pad=20.0)
        plt.savefig('daily caloric supply.pdf',bbox_inches='tight')
        plt.show()
    
    def boxPlot_for_dailyCaloricSupply(self):
        '''
        foodGroup: Sugar, Oils, fats...
        Extract the main food groups from file 
        Plot a box plot to show daily caloric supply of different food groups
        '''
        df=self.foodGroup
        new_df = df.loc[:,['Sugar (kilocalories per person per day)',
                           'Oils & Fats (kilocalories per person per day)',
                           'Meat (kilocalories per person per day)',
                           'Dairy & Eggs (kilocalories per person per day)',
                           'Fruits & Vegetables (kilocalories per person per day)',
                           'Cereals & Grains (kilocalories per person per day)']]
        sns.set_style("whitegrid")  
        
        # add grid
        ax = sns.boxplot(data=new_df,orient="h",width=0.8,palette=[self._color]*6,fliersize=1) 
        
        for patch in ax.artists:                   
            r, g, b, a = patch.get_facecolor()
            # change transparency
            patch.set_facecolor((r, g, b, self._transparency))
        
        # graph the plot
        ax.tick_params(axis='x',labelsize=self._fontsize)
        plt.rcParams["figure.figsize"] = [12, 4.8]
        ax.set_yticklabels(labels=['Sugar',
                                   'Oils & Fats',
                                   'Meat',
                                   'Dairy & Eggs',
                                   'Fruits & Vegetables',
                                   'Cereals & Grains'],fontsize=self._fontsize)
        plt.xlabel('kilocalories per person per day',fontsize=self._fontsize)
        plt.savefig('box2.pdf',bbox_inches='tight')
        plt.show()
    
    def lineChart_for_fruit_vegetable_meat_intake(self, files):
        '''
        Plot a line chart to compare the value of fruit/vegetable/meat intake(kg/capita/yr) 
        from 1961 to 2013 of four countries
        param: files --> list of items you want to plot
        type: list
        '''
        # make sure 'files' is the correct data type and only contains string 
        assert isinstance(files, list)
        assert all(isinstance(item, str) for item in files)

        countries = ['India', 'Russia', 'China', 'United States']
        plt.rcParams["figure.figsize"] = [8, 4.8]
        year = []
        
        # set x-axis
        for i in range(1961,2014,10):
            year.append(i)
        
        # plot fruit, vegetable, and meat graph for three countries
        for i in files:
            
            # clean data for fruit
            if i=='fruit':
                print(i)
                col_name = ' (kilograms per person)'
                df = self.fruit
            elif i=='vegetable':
                print(i)
                col_name = 'Food Balance Sheets: Vegetables - Food supply quantity (kg/capita/yr) (FAO (2017)) (kg)'
                df = self.vegetable
            else:
                print(i)
                col_name = 'Value'
                df = self.meat
            
            # clean data for meat
            if i=='meat':
                y1 = df[df.Country=='India']
                y2 = df[df.Country=='China']
                y3=df[df.Country=='United States of America']
                y4=df[df.Country=='Russian Federation']
                y5=df[df.Country=='USSR']
            
            # clean data for meat
            else:
                y1 = df[df.Entity=='India']
                y2 = df[df.Entity=='China']
                y3=df[df.Entity=='United States']
                y4=df[df.Entity=='Russia']
                y5=df[df.Entity=='USSR']
            
            y6 = list(y5[col_name])+list(y4[col_name])
            
            # plot the graph
            plt.clf()
            plt.plot(range(1961,2014),list(y1[col_name]),marker='.',label='India')
            plt.plot(range(1961,2014),list(y2[col_name]),marker='.',label='China')
            plt.plot(range(1961,2014),list(y3[col_name]),marker='.',label='United States')
            plt.plot(range(1961,2014),y6,marker='.',label='Russia')
            plt.legend(loc='best')
            plt.xticks(year) 
            plt.xlim(1961, 2013)
            plt.grid()
            plt.savefig('line_{}.pdf'.format(i),bbox_inches='tight')
            plt.show()
    
    def barPlot_dietary_component_for_four_countries(self):
        '''
        Compare the main food group intake of four countries
        Compute the mean intake for 6 food groups
        '''
        df = self.diet
        grp = df.groupby('Entity')
        res=grp.mean()
        countries = ['India','Russia', 'China','United States']
        new_df=res.loc[countries,:]
        new_df = new_df.loc[:,['Sugar (kilocalories per person per day)',
                               'Oils & Fats (kilocalories per person per day)',
                               'Meat (kilocalories per person per day)',
                               'Dairy & Eggs (kilocalories per person per day)',
                               'Fruits & Vegetables (kilocalories per person per day)',
                               'Cereals & Grains (kilocalories per person per day)']]
        
        ax=new_df.plot.bar(stacked=False, alpha=0.9)
        ax.set(ylim=[0, 1500])
        plt.xticks(x=countries, rotation=0)
        ax.legend(['Sugar',
                   'Oils& Fats',
                   'Meat',
                   'Dairy& Eggs',
                   'Fruits & Vegetables',
                   'Cereals & Grains'])
        plt.ylabel('kilocalories per person per day')
        plt.savefig('kilocalories per person per day2.pdf',bbox_inches='tight')
        plt.show()
    
    def lineChart_food_consumption(self, start_zero=False):
        '''
        Graph the global food consumption  trend in 4 major categories:
        Carbs, Vegetable, Fruit, Meat, Seafood
        param: start_zero --> whether to center all graph at the origin
        type: bool
        '''
        # assert start_zero is the correct datatype
        assert isinstance(start_zero, bool)

        # select useful data
        df = self.food[['Item','Year','Value']]
        
        # combine data in cereal and starchy roots
        df_cereal = df.loc[df['Item'] == 'Cereals - Excluding Beer']
        df_starchy = df.loc[(df['Item'] == 'Starchy Roots')]
        
        # reassign index
        df_cereal.index = range(len(df_cereal))
        df_starchy.index = range(len(df_starchy))

        # add values together, creating carb_value
        carb_value = df_cereal['Value'] + df_starchy['Value']
     
        # Extract data for plotting: vegetable, fruit, meat, carbs
        df_veg = df.loc[df['Item'] == 'Vegetables']
        df_meat = df.loc[df['Item'] == 'Meat']
        df_seafood = df.loc[df['Item'] == 'Fish, Seafood']
        df_fruit = df.loc[df['Item'] == 'Fruits - Excluding Wine']
        df_carb = carb_value.to_frame()
        df_carb['Year'] = df_cereal['Year']
        
        def sum_over_year(data, start_zero=start_zero):
            '''
            Sum all values over every year. ie. how much 
            param: data --> DataFrame you input
            return: list of all values from 1961 to 2013
            '''
            # create year list
            year_list = list(range(1961,2014))
            value = []
            
            # sum all values of the same year
            for year in year_list:
                year_sum = data['Value'][data['Year'] == year].sum()
                value.append(year_sum/(10**3))
            
            # zero center all the data if zero_center == True
            if start_zero == True:
                first_value = value[0]
                value_new = [item-first_value for item in value]
                return value_new
            else:
                return value
        
        # compute the value based on start_zero or not
        if start_zero == False:
            # compute the data, sum all values every year
            veg_value = sum_over_year(df_veg)
            meat_value = sum_over_year(df_meat)
            seafood_value = sum_over_year(df_seafood)
            fruit_value = sum_over_year(df_fruit)
            carb_value = sum_over_year(df_carb)
            # set opacity, and special condition
            opacity = 1
            condition = 'normal'
        else:
            # compute the data, sum all value every year. Starts at zero
            veg_value = sum_over_year(df_veg, start_zero)
            meat_value = sum_over_year(df_meat, start_zero)
            seafood_value = sum_over_year(df_seafood, start_zero)
            fruit_value = sum_over_year(df_fruit, start_zero)
            carb_value = sum_over_year(df_carb, start_zero)
            # set opacity 
            opacity = 0.07
            condition = 'start_at_zero'
        
        # graph line chart
        year = list(range(1961, 2014))
        plt.plot(year, veg_value, color='g', label='Vegetable')
        plt.plot(year, meat_value, color='r', alpha=opacity, label='Meat')
        plt.plot(year, seafood_value, color='blue',alpha=opacity, label='Seafood')
        plt.plot(year, fruit_value, color='orange', label='Fruit')
        plt.plot(year, carb_value, color='purple', alpha=opacity, label='Carbohydrate')
        # set legend and axis
        plt.legend(bbox_to_anchor=(1.04,1), loc="upper left", frameon=False)
        plt.xlabel('Year')
        plt.ylabel('Consumption (million tons)')
        plt.grid(alpha=0.5)
        plt.savefig('Global Food Consumption-%s.pdf' %(condition), bbox_inches='tight')
        plt.show()
    
    def initial_style_pyecharts(self):
        '''
        Initialize the style of the charts
        Set the appropriate parameters
        width: the width of the output image
        height: the height of the output image
        background_color: let it as black
        '''
        style = Style(
        title_color="#fff",
        #title_pos="center",
        width=1400,
        height=800,
        background_color='#bbb'
        )
        return style
    
    def dataloader(self):
        '''
        Extract csv files from the zip files
        Read csv files
        '''
        from zipfile import ZipFile
        myzip1=ZipFile('data/FoodSupply_Crops_E_All_Data.zip')
        f1=myzip1.open('FoodSupply_Crops_E_All_Data.csv')
        self.df_crops=pd.read_csv(f1,encoding = "ISO-8859-1")
        self.df_crops=np.matrix(self.df_crops.values)
        f1.close()
        myzip1.close()
        myzip2=ZipFile('data/FoodSupply_LivestockFish_E_All_Data.zip')
        f2=myzip2.open('FoodSupply_LivestockFish_E_All_Data.csv')
        self.df_meats=pd.read_csv(f2,encoding = "ISO-8859-1")
        self.df_meats=np.matrix(self.df_meats.values)
        f2.close()
        myzip2.close()
        
    def generate_map(self,style):
        '''
        Generate the corresponding world map according to the data we have
        This function will directly save the charts as 'distribution.html' in this folder
        param: style --> output of style function
        output: save 'distribution.html' in the same folder
        '''
        # make sure input style is the right type: pyecharts.Style
        assert isinstance(style, pyecharts.Style)

        # set up countries map
        countries=np.ndarray.flatten(np.array(self.df_crops[:,1]).astype(np.str)).tolist()
        countries=set(countries)
        veg_con=[]
        healthy_veg_con=[]
        countries=sorted(countries)
        
        # time line for every year
        for j in range(53):
            one_year_con=[]
            health_oyc=[]
            # calculate value for each country
            for i in countries:
                ind1=np.intersect1d((np.where(self.df_crops[:,1]==i))[0],
                                    (np.where(self.df_crops[:,3]=='Vegetables'))[0])
                temp=self.df_crops[ind1]
                ind2=(np.where(temp[:,4]==645))[0]
                one_year_con.append(np.ndarray.flatten(temp[ind2]).tolist()[0][7+j*2])
                health_oyc.append((np.ndarray.flatten(temp[ind2]).tolist()[0][7+j*2])>85)
                
            one_year_con.append(one_year_con[countries.index('Denmark')])
            health_oyc.append(health_oyc[countries.index('Denmark')])
            veg_con.append(one_year_con)
            healthy_veg_con.append(health_oyc)
        countries[countries.index('United States of America')]='United States'
        countries[countries.index('Russian Federation')]='Russia'
        countries.append('Greenland')
        
        # connect USSR data. USSR: 1961-1991, Russia: 1992-2013
        for i in range(31):
            veg_con[i][countries.index('Russia')]=veg_con[i][countries.index('USSR')]
        maps=[]
        years=[1961+i for i in range(53)]
        timeline = Timeline(is_auto_play=False, timeline_bottom=0, timeline_play_interval=50,width=1100)
        
        # graph the world map
        for i in range(53):
            MAP = Map("world map", **style.init_style)
            MAP.add("world map", countries, veg_con[i], 
                    maptype="world",  
                    is_visualmap=True, 
                    visual_range=[0,200],
                    visual_text_color='#fff', 
                    visual_top=50, 
                    is_map_symbol_show=False)
            timeline.add(MAP,str(years[i]))
            
        # render timeline
        timeline.render(path='distribution.html')
        
    def generate_pie(self,country):
        '''
        Generate the corresponding pie charts
        param: country --> the country we want to use in the dataset
        type: str
        output: save the pie chart as 'country.html' in this folder
        '''
        # make sure country is a string
        assert isinstance(country, str)

        # extract the data we need
        attr1=np.ndarray.flatten(np.array(self.df_crops[:,3]).astype(np.str)).tolist()
        attr1=set(attr1)
        attr2=np.ndarray.flatten(np.array(self.df_meats[:,3]).astype(np.str)).tolist()     
        attr2=set(attr2)
        composition1={'Vegetables':0,
                      'Fruits - Excluding Wine':0, 
                      'Cereals - Excluding Beer':0}
        composition2={'Meat':0, 'Milk, Whole':0}
        
        # graph Vegetables, Fruits, Cereals
        for i in composition1.keys():
            ind1=np.intersect1d((np.where(self.df_crops[:,1]==country))[0],
                                (np.where(self.df_crops[:,3]==i))[0])
            temp=self.df_crops[ind1]
            ind2=(np.where(temp[:,4]==645))[0]
            #print(np.ndarray.flatten(temp[ind2]).tolist()[0][107])
            composition1[i]=(np.ndarray.flatten(temp[ind2]).tolist()[0][7+51*2])
        
        # graph Meat, Milk
        for i in composition2.keys():
            ind1=np.intersect1d((np.where(self.df_meats[:,1]==country))[0],
                                (np.where(self.df_meats[:,3]==i))[0])
            temp=self.df_meats[ind1]
            ind2=(np.where(temp[:,4]==645))[0]
            composition2[i]=(np.ndarray.flatten(temp[ind2]).tolist()[0][7+51*2])
        
        # create variables for pie chart
        attr=[]
        v1=[]
        for i,j in composition1.items():
            attr.append(i)
            v1.append(j)
        for i,j in composition2.items():
            attr.append(i)
            v1.append(j)
        
        # graph pie chart
        pie = Pie("Diet")
        pie.add("", attr, v1, is_label_show=True, center=[50,50], rosetype = 'radius')
        pie.render(path=country+'.html')
