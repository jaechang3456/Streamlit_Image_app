import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import pandas as pd
import os
from datetime import datetime

def save_uploaded_file(directory, img):
    # 1. 디렉토리가 있는지 확인하여, 없으면 만든다.
    if not os.path.exists(directory) :
        os.makedirs(directory)
    # 2. 이제는 디렉토리가 있으니까, 파일을 저장
    filename = 'yeonhee' + datetime.now().isoformat().replace(':','-').replace('.','-')
    img.save(directory + '/' + filename + '.jpg')
    return st.success("Saved file : {} in {}".format(filename + '.jpg' , directory))

def load_image(Image_file) :
    img = Image.open(Image_file)
    return img


def main():
    
    st.title('여러 파일을 업로드하는 앱')
    # 사이드바 메뉴
    menu = ['Image',"Dataset",'About']
    choice = st.sidebar.selectbox("메뉴",menu)
    print(choice)

    if choice =='Image':
        uploaded_files = st.file_uploader("이미지 파일 업로드",type=['png','jpeg','jpg'],accept_multiple_files=True)
        print(uploaded_files)

        if uploaded_files is not None :

            # 2. 각 파일을 이미지로 바꿔줘야 한다.
            image_list = []

            # 2-1. 모든 파일이, image_list에 이미지로 저장됨
            for img_file in uploaded_files:
                img = load_image(img_file)
                image_list.append(img)

            # 3. 이미지를 화면에 확인해 본다.
            # for img in image_list :
            #     st.image(img)

        option_list2 = ['Show Image','Rotate Image','Create Thumbnail',
        'Crop Image','Merge Images','Change Color','Filters - Edge Enhance','Flip Image','Contrast Image']
        
        option2 = st.selectbox("옵션을 선택하세요.",option_list2)

        if option2 == 'Show Image':
            for img in image_list :
                st.image(img)

            directory = st.text_input('파일 경로 입력')

            if st.button('파일 저장') :
                for img in image_list :
                    save_uploaded_file(directory,img)

        elif option2 == 'Rotate Image':
            # 1. 유저가 입력
            degree = st.number_input('각도 입력',0,360)
            # 2. 모든 이미지를 돌린다.
            transformed_img_list = [ ]
            for img in image_list :
                rotated_img = img.rotate(degree)
                st.image(rotated_img)
                transformed_img_list.append(rotated_img)
            
            directory = st.text_input('파일 경로 입력')

            if st.button('파일 저장') :
                # 3. 파일 저장.
                for img in transformed_img_list :
                    save_uploaded_file(directory,img)


        elif option2 == 'Create Thumbnail':
            # 1. 이미지의 사이즈를 알아야 겠다.
            
            st.write(img.size)
            
            width = st.number_input('width 입력',1,100)
            height = st.number_input('height 입력',1,100)

            size = (width,height)

            transformed_img_list = [ ]

            for img in image_list :
                img.thumbnail(size)
                st.image(img)
                transformed_img_list.append(img)
                #저장은 여기서
            directory = st.text_input('파일 경로 입력')

            if st.button('파일 저장') :
                # 3. 파일 저장.
                for img in transformed_img_list :
                    save_uploaded_file(directory,img)

        
        elif option2 == 'Crop Image':
            #왼쪽 위부분 부터, 오른쪽 아래 부분까지 잘라라
            #왼쪽 위부분 좌표(50 100)
            #너비 X축으로,깊이 y축으로 계산한 종료 좌표 (200,200)   
            #시작좌표 + (너비,높이) => 크탑 종료 좌표
            start_x = st.number_input('시작 x 좌표 입력',0,img.size[0]-1)
            start_y = st.number_input('시작 y 좌표 입력',0,img.size[1]-1)
            max_width = img.size[0] - start_x
            max_height = img.size[1] - start_y
            width = st.number_input('width 입력',1,max_width)
            height = st.number_input('height 입력',1,max_height)
            
            box = (start_x,start_y,start_x + width,start_y + height)
            cropped_img = img.crop(box)
            cropped_img.save('data/crop.png')
            st.image(cropped_img)

        elif option2 == 'Merge Images':

            merge_file = st.file_uploader("Upload Image", type=['png','jpg','jpeg'], key='merge')

            if merge_file is not None :

                merge_img = load_image(merge_file)
            
                start_x = st.number_input('시작 x 좌표 입력',0,img.size[0])
                start_y = st.number_input('시작 y 좌표 입력',0,img.size[1])
            
                position = (0,200)
                img.paste(merge_img,position)
                st.image(img)

        elif option2 == 'Flip Image' :

            status = st.radio('플립 선택', ['FLIP_TOP_BOTTOM', 'FLIP_LEFT_RIGHT'])

            if status == 'FLIP_TOP_BOTTOM' :
                transformed_img_list = [ ]
                for img in image_list :
                    flipped_img = img.transpose( Image.FLIP_TOP_BOTTOM)
                    st.image(flipped_img)
                    transformed_img_list.append(flipped_img)
            elif status == 'FLIP_LEFT_RIGHT' :
                transformed_img_list = [ ]
                for img in image_list :
                    flipped_img = img.transpose( Image.FLIP_LEFT_RIGHT)
                    st.image(flipped_img)
                    transformed_img_list.append(flipped_img)

            directory = st.text_input('파일 경로 입력')

            if st.button('파일 저장') :
                # 3. 파일 저장.
                for img in transformed_img_list :
                    save_uploaded_file(directory,img)
  

        elif option2 == 'Change Color':

            status = st.radio('색 변경', ['Color', 'Gray Scale', 'Black & White'])

            if status == 'Color' :
                color = 'RGB'
            elif status == 'Gray Scale' :
                color = 'L'
            elif status == 'Black & White' :
                color = '1'

            bw = img.convert(color)
            st.image(bw)

            directory = st.text_input('저장할 디렉토리를 입력하세요.')

            if not os.path.exists(directory) :
                os.makedirs(directory)
                file_name = st.text_input('저장할 파일 이름을 입력하세요.')
                st.button('파일저장')
                bw.save(directory + '/' + file_name + '.png' )

            elif os.path.exists(directory) :
                file_name = st.text_input('저장할 파일 이름을 입력하세요.')
                st.button('파일저장')
                bw.save(directory + '/' + file_name + '.png' )

        elif option2 == 'Contrast Image' :
            contrast_img = ImageEnhance.Contrast(img).enhance(2)
            st.image(contrast_img)

            directory = st.text_input('저장할 디렉토리를 입력하세요.')

            if not os.path.exists(directory) :
                os.makedirs(directory)
                file_name = st.text_input('저장할 파일 이름을 입력하세요.')
                st.button('파일저장')
                contrast_img.save(directory + '/' + file_name + '.png' )

            elif os.path.exists(directory) :
                file_name = st.text_input('저장할 파일 이름을 입력하세요.')
                st.button('파일저장')
                contrast_img.save(directory + '/' + file_name + '.png' )

        elif option2 == 'Filters - Edge Enhance':
            edge_img = img.filter(ImageFilter.EDGE_ENHANCE)
            st.image(edge_img)

            directory = st.text_input('저장할 디렉토리를 입력하세요.')

            if not os.path.exists(directory) :
                os.makedirs(directory)
                file_name = st.text_input('저장할 파일 이름을 입력하세요.')
                st.button('파일저장')
                edge_img.save(directory + '/' + file_name + '.png' )

            elif os.path.exists(directory) :
                file_name = st.text_input('저장할 파일 이름을 입력하세요.')
                st.button('파일저장')
                edge_img.save(directory + '/' + file_name + '.png' )           
            


    # 3. 여러파일을 변환할 수 있도록 수정. 각 옵션마다 저장하기 버튼이 있어서,
    # 버튼 누르면 저장되도록, 저장시에는, 디렉토리이름을 유저가 직접 입력하여 저장.

    

if __name__ == '__main__':
    main()