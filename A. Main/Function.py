import matplot


def gradient_mapper(metric,grad):
    
    '''
    This function outputs a list of colors that corresponds to each item in a list/series of numbers.
    This will be used to color our state map heatmap.
    
    Parameters:
    - metric - the data that we are transforming into colors
    - grad - list of colors that the metric data will be transformed to
    
    '''
    # Define the minimum and the maximum points in the dataset
    metric_min = metric.min()
    metric_max = metric.max()

    # Calculate how many colors we have in the given gradient color scheme
    colors = len(grad)-1
    
    # Transform the data to integers between zero and the length of the gradient list
    first_map = list(map(lambda x: int(round(colors*(x-metric_min) / (metric_max-metric_min),0)), list(metric)))
    
    # Map the integers to the gradient list, which is what will be used to color the state heatmaps
    return list(map(lambda x: grad[x], first_map))



def state_map(metric, grad, title, states = list(states_data.index), annot=True,
              pacific=True, dc=True, size=30, cb=True):
    
    '''
    Create a map of the states that has a color gradient based on a given metric for each state.
    
    Parameters:
    - metric - Column data we will use to identify the coloring of the map. 
            The column must be from the states_data dataframe.
    - grad - The color scheme we will use to color our map.
    - title - Title for the chart
    - states - List of state that we want to map (based on state abbreviations).
    - annot - If true this will write state names and corresponding metric values on the map. 
                If false no labels will be displayed.
    - pacific - Will include the pacific states (Hawaii and Alaska) in the bottom left corner of the chart if true.
    - size - Set the plot width (height will auto-adjust).
    - cb - If true will include a color bar as a key.
    
    '''
   
    # Create a temporary dataframe that contains the state abbreviations as an index 
    # and the geometry of each state with corresponding metric values:
    data_temp = states_data.loc[states,['geometry',metric]]
    
    # Drop states that have null values:
    data_temp = data_temp.dropna()
    
    # Create local varaibles for pacific and mainland states:
    pacific_states = ['AK','HI']
    mainland_states = list(filter(lambda x: x not in pacific_states,
                              list(data_temp.index)))
    
    # If no values for DC or pacific states, remove from our temporary dataframe:
    if dc == False and dc in states:
        data_temp = data_temp.drop('DC')
        mainland_states.remove('DC')
        
    if pacific == False and 'HI' in states and 'AK' in states:
        data_temp = data_temp.drop(['HI','AK'])
    
    # Use the gradient_mapper function to add the color gradient based on metric values:
    data_temp['Colors'] = gradient_mapper(metric=data_temp[metric],grad=grad)
        
    # Create a figure and axes for our chart:
    fig, ax = plt.subplots(figsize=(size,size/2))
    plt.title(title, fontsize=30)
    
    
    # First, plot the mainland states 
    for i in mainland_states:
        data_temp.loc[[i]].plot(ax=ax, color=data_temp.loc[i,'Colors'])
                
        # Indicate necessary data for if we are annotating:
        if annot == True:
            
            # Locate the location we want to plot text (the center of each state):
            centroid = data_temp.loc[[i]].centroid
            
            # Plot the text in this location:
            plt.annotate(s=f'{round(data_temp.loc[i,metric],1)}',
                 xy=(centroid.x[i], centroid.y[i]),
                 horizontalalignment='center',
                 color='white',
                 fontsize=size/2)
            
    # Remove axes ticks
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Second, plot the Pacific states in their own separate subplots
    if pacific == True:
        if 'AK' in states:
            ax2 = fig.add_subplot(3,6,13)
            states_data.loc[['AK']].plot(ax=ax2,
                                       color=data_temp.loc['AK','Colors'])
            ax2.patch.set_alpha(0)
            ax2.set_xticks([])
            ax2.set_yticks([])
        
        if 'HI' in states:
            ax3 = fig.add_subplot(3,6,14)
            states_data.loc[['HI']].plot(ax=ax3,
                                       color=data_temp.loc['HI','Colors'])
            ax3.patch.set_alpha(0)
            ax3.set_xticks([])
            ax3.set_yticks([])
        
    # Third, plot the colorbar key
    if cb == True:        
        cmap = LinearSegmentedColormap.from_list(name= '', colors=grad, N=50)
        ax4 = fig.add_subplot(1,30,30)
        norm = mpl.colors.Normalize(vmin=data_temp[metric].min(),
                                    vmax=data_temp[metric].max())
        cb = mpl.colorbar.ColorbarBase(ax4, cmap=cmap,
                                       norm=norm, orientation='vertical')
           
    sns.despine(left=True,bottom=True)