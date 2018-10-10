import numpy as np
import imageio
import matplotlib.pyplot as plt
import os

# TODO make axis object accessible from outside to create versatility, like plotting titles and axis names

class Arrow():
    def __init__(self, ori_over_time, vector_over_time, alpha_over_time=1, text='', text_shift=[0,0], color='black'):
        self.looks_dict = {'head_width':0.05, 'head_length':0.1, 'fc':color, 'ec':color, 'length_includes_head':True}
        if (len(np.array(ori_over_time).shape) != 2) or (len(np.array(vector_over_time).shape) != 2):
            raise Exception('Please provide 2D coordinates over time (first dim)')
        self.ori_over_time = ori_over_time; self.vector_over_time = vector_over_time
        self.alpha_over_time = alpha_over_time
        self.color = color
        self.text_coordinates_over_time = np.array(ori_over_time) + 0.5*np.array(vector_over_time) + np.array(text_shift)
        self.text = text

class Animation():
    def __init__(self, n_frames=80, dpi=150, fps=15, figsize=(2.2,1.7), size=[0, 2.5, 0, 2.5]):
        self.dpi=dpi; self.fps=fps; self.figsize=figsize; self.n_frames=n_frames
        self.size=size
        self.arrows = []
        self.texts = []
    
    def create_fractional_timing(self, zeros, ramp, ones):
        fractional_timing = np.array([0]*zeros + list(np.linspace(0,1,ramp)) + [1]*ones)
        if len(fractional_timing) != self.n_frames:
            raise Exception('Input is inconsistent with number of frames in animation!')
        return fractional_timing
    
    def create_axis(self, ax):
        axis = {'fc':'k', 'ec':'k', 'head_width':0.05,  'head_length':0.1, 'clip_on':False, 'length_includes_head':True}
        for side in ['bottom','right','top','left']:
            ax.spines[side].set_visible(False)
        ax.arrow(self.size[0], 0, self.size[1], 0, **axis);
        ax.arrow(0, self.size[2], 0, self.size[3], **axis);
        ax.set_xticks([]); ax.set_yticks([]);
        
    def format_plot(self, ax):
        self.create_axis(ax)
        ax.set_xlim(self.size[0], self.size[1])
        ax.set_ylim(self.size[2], self.size[3])
        
    def add_arrows(self, arrows):
        self.arrows.extend(arrows)
        
    def render_animation(self, output='hallo.gif'):
        with imageio.get_writer(output, mode='I', fps=self.fps) as writer:
            for frame in np.arange(self.n_frames):
                fig,ax = self.render_frame(frame)                
                plt.savefig('tmp.png');
                plt.close(fig);
                image = imageio.imread('tmp.png');
                writer.append_data(image);
            os.remove('tmp.png')

    def render_frame(self, frame=0):
        if frame>=self.n_frames:
            print("Input 'frame' higher than number of frames!"); return
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        for arrow in self.arrows:
            ori = arrow.ori_over_time[frame]; vec = arrow.vector_over_time[frame]
            text_coord = arrow.text_coordinates_over_time[frame]
            ax.arrow(ori[0],ori[1],vec[0],vec[1], **arrow.looks_dict)
            ax.text(text_coord[0], text_coord[1], arrow.text)
        self.format_plot(ax)
        return fig,ax