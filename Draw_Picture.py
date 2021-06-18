# -*- coding:utf-8 -*-
from pyecharts import options as opts
from pyecharts.charts import Line,Pie,Grid
from pyecharts.commons.utils import JsCode

import os
import Excel_Analyser
#import imgkit

#path_wkimg = r'D:\Software_install_data\wkhtmltox\wkhtmltopdf\bin\wkhtmltoimage.exe'  # 工具路径
#cfg = imgkit.config(wkhtmltoimage=path_wkimg) #转换类型

class Picture_Drawer(object):

  def dray_line_piture(self,my_line_data_x,my_line_data_y):

      if os.path.isfile('.\line_color.html'):
        os.remove('.\line_color.html')
      if(len(my_line_data_x) != len(my_line_data_y)):
          print("leng not match !!!")
          exit()
      x_data = my_line_data_x
      y_data = my_line_data_y

      #print(x_data)
      #print(y_data)
      background_color_js = (
          "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
          "[{offset: 0, color: '#c86589'}, {offset: 1, color: '#06a7ff'}], false)"
      )
      area_color_js = (
          "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
          "[{offset: 0, color: '#eb64fb'}, {offset: 1, color: '#3fbbff0d'}], false)"
      )

      c = (
          Line(init_opts=opts.InitOpts(bg_color=JsCode(background_color_js)))
              .add_xaxis(xaxis_data=x_data)
              .add_yaxis(
              series_name="注册总量",
              y_axis=y_data,
              is_smooth=True,
              is_symbol_show=True,
              symbol="circle",
              symbol_size=6,
              linestyle_opts=opts.LineStyleOpts(color="#fff"),
              label_opts=opts.LabelOpts(is_show=True, position="top", color="white",formatter="{c}%"),
              itemstyle_opts=opts.ItemStyleOpts(
                  color="red", border_color="#fff", border_width=3
              ),
              tooltip_opts=opts.TooltipOpts(is_show=False),
              areastyle_opts=opts.AreaStyleOpts(color=JsCode(area_color_js), opacity=1),
          )
              .set_global_opts(
              title_opts=opts.TitleOpts(
                  title="Yield",
                  pos_left="5%",
                  pos_top="5%",
                  title_textstyle_opts=opts.TextStyleOpts(color="#fff", font_size=16),
              ),
              xaxis_opts=opts.AxisOpts(
                  type_="category",
                  boundary_gap=False,
                  axislabel_opts=opts.LabelOpts(margin=30, color="#ffffff63"),
                  axisline_opts=opts.AxisLineOpts(
                      #is_show=False,
                      linestyle_opts=opts.LineStyleOpts(width=2, color="#fff")
                  ),
                  axistick_opts=opts.AxisTickOpts(
                      is_show=True,
                      length=25,
                      linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                  ),
                  splitline_opts=opts.SplitLineOpts(
                      is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                  ),
              ),
              yaxis_opts=opts.AxisOpts(
                  type_="value",
                  position="right",
                  axislabel_opts=opts.LabelOpts(margin=20, color="#ffffff63"),
                  axisline_opts=opts.AxisLineOpts(
                      linestyle_opts=opts.LineStyleOpts(width=2, color="#fff")
                  ),
                  axistick_opts=opts.AxisTickOpts(
                      is_show=False,
                      length=15,
                      linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                  ),
                  splitline_opts=opts.SplitLineOpts(
                      is_show=False, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                  ),
              ),
              legend_opts=opts.LegendOpts(is_show=False),
          )
              .render("line_color.html")
      )

  def draw_rose_piture(self,my_rose_data):
    total_position = 0
    for x in my_rose_data:
      total_position = total_position + x[1]
    #print(total_position)
    if os.path.isfile('pie_rosetype.html'):
       os.remove('.\pie_rosetype.html')
    c = (
        Pie()
        .add(
            "",
            my_rose_data,
            radius=["30%", "75%"],
            #center=["25%", "50%"],
            rosetype="radius",
            #label_opts=opts.LabelOpts(is_show=False),
        )
        #.add(
        #    "",
        #    my_rose_data,
        #    radius=["30%", "75%"],
        #    center=["75%", "50%"],
        #    rosetype="area",
        #)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Positions",pos_left="8%",pos_top="8%"),
            graphic_opts=[
                opts.GraphicGroup(
                    graphic_item=opts.GraphicItem(
                        # 控制整体的位置
                        right="15%",
                        bottom="5%",
                    ),
                    children=[
                        # opts.GraphicRect控制方框的显示
                        # 如果不需要方框，去掉该段即可
                        #opts.GraphicRect(
                        #    graphic_item=opts.GraphicItem(
                        #        z=100,
                        #        right="center",
                        #        bottom="middle",
                        #    ),
                        #    graphic_shape_opts=opts.GraphicShapeOpts(
                        #        width=120, height=70,
                        #    ),
                        #    graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                        #        fill="#fff",
                        #        stroke="#555",
                        #        line_width=2,
                        #        shadow_blur=8,
                        #        shadow_offset_x=3,
                        #        shadow_offset_y=3,
                        #        shadow_color="rgba(144,238,144,0.3)",
                        #    )
                        #),
                        # opts.GraphicText控制文字的显示
                        opts.GraphicText(
                            graphic_item=opts.GraphicItem(
                                left="center",
                                top="middle",
                                z=100,
                            ),
                            graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                                # 可以通过jsCode添加js代码，也可以直接用字符串
                                text="Tatal:"+str(total_position)+"%",
                                font="bolder 21px Microsoft YaHei",
                                graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                    fill="#C537B6"
                                )
                            )
                        )
                    ]
                )
            ]
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b} {c}%"))
        .render("pie_rosetype.html")
    )
    #imgkit.from_file(r'./pie_rosetype.html','pie_rosetype.jpg',config=cfg)

if __name__=="__main__":
    my_drawer = Picture_Drawer()
    my_excel_analyser0 = Excel_Analyser.excel_analyser()
    #my_data = []
    #my_data.append(("haha", 70))
    #my_data.append(("阿嫩", 40))
    #my_data.append(("上证50", 130))
    #my_data.append(("沪深300", 130))
    #print(my_data)
    #my_rose_picture = my_drawer.draw_rose_piture(my_data)
    my_x_data,my_y_data = my_excel_analyser0.yield_analyse(r'.\yield.xlsx')
    #my_x_data = ["05-11", "05-19", "05-20"]
    #my_y_data = [0, 0.23, 0.034]
    my_line_picture = my_drawer.dray_line_piture(my_x_data,my_y_data)
