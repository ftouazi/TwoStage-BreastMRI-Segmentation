import segmentation_models_pytorch as smp

def get_seg_model(name="unetplusplus", encoder_name="resnet34", in_channels=1, out_channels=1):
    name = name.lower()
    if name in ["unet","unet++","unetplusplus","unet2+","unetpp"]:
        return smp.UnetPlusPlus(encoder_name=encoder_name, in_channels=in_channels, classes=out_channels)
    if name in ["unet3+","unet3plus"]:
        # segmentation_models_pytorch does not include UNet3+; placeholder uses Unet
        return smp.Unet(encoder_name=encoder_name, in_channels=in_channels, classes=out_channels)
    if name in ["attentionunet","attention_unet"]:
        # use Unet with attention? placeholder uses Unet
        return smp.Unet(encoder_name=encoder_name, in_channels=in_channels, classes=out_channels)
    if name in ["transunet","trans_unet"]:
        # placeholder: use Unet
        return smp.Unet(encoder_name=encoder_name, in_channels=in_channels, classes=out_channels)
    return smp.Unet(encoder_name=encoder_name, in_channels=in_channels, classes=out_channels)
