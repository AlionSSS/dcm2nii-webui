import SimpleITK as sitk
import os
import zipfile


def dicom_to_nii(dicom_dir_path: str, nii_file_path: str):
    """
    dicom文件转nii文件
    :param dicom_dir_path: dicom文件目录
    :param nii_file_path: 转换后要保存的nii文件路径
    :return: None
    """
    # 读取 dicom
    reader = sitk.ImageSeriesReader()
    img_name = reader.GetGDCMSeriesFileNames(dicom_dir_path)
    reader.SetFileNames(img_name)
    image = reader.Execute()
    # 转为 nii.gz
    image_array = sitk.GetArrayFromImage(image)
    image_out = sitk.GetImageFromArray(image_array)
    image_out.SetOrigin(image.GetOrigin())
    image_out.SetSpacing(image.GetSpacing())
    image_out.SetDirection(image.GetDirection())
    # 保存nii.gz文件到配置的目录下
    nii_dir_path = os.path.dirname(nii_file_path)
    if not os.path.exists(nii_dir_path) or not os.path.isdir(nii_dir_path):
        os.mkdir(nii_dir_path)
    sitk.WriteImage(image, nii_file_path)


def unzip_dicom_file(zip_file_path: str, save_dir_path: str):
    with zipfile.ZipFile(zip_file_path, "r") as zfile:
        # 文件名包含中文时有乱码问题
        zfile.extractall(save_dir_path)

        # 找到存放dicom文件的目录
        # 如果存在名称为dicom的目录，直接就用
        for info in zfile.infolist():
            if info.is_dir() and info.filename == "dicom":
                return info.filename
        # 否则获取第一个目录，排除MAC上的固定目录
        for info in zfile.infolist():
            if info.is_dir() and not info.filename == "__MACOSX/":
                return info.filename
        # 如果还是找不到，就直接用当前目录
        return "."
