# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/capsule.ipynb.

# %% auto 0
__all__ = ["to", "train", "validate", "predict", "Capsule"]

# %% ../../nbs/capsule.ipynb 2
from functools import wraps
from ..loader import *
from ..torch_loader import *
from ..paths import loaddill, dumpdill, makedir, parent
from ..load_defaults import exists
from ..markup import AttrDict

try:
    import mmcv
    from mmcv.parallel.data_container import DataContainer
except ImportError:
    DataContainer = None

# %% ../../nbs/capsule.ipynb 3
def to(item, device):
    if item is None:
        return None
    elif isinstance(item, (torch.Tensor, nn.Module)):
        return item.to(device)
    elif isinstance(item, (AttrDict, dict)):
        return type(item)({k: to(v, device) for k, v in item.items()})
    elif isinstance(item, (list, tuple)):
        return type(item([to(_item, device) for _item in item]))
    elif DataContainer is not None and isinstance(item, DataContainer):
        return DataContainer([to(_item, device) for _item in item.data])
    else:
        # logger.warning(f"function is not implemented for {type(item)}")
        return item
        raise NotImplementedError(f"function is not implemented for {type(item)}")


def train(train_function):
    @wraps(train_function)
    def _train_batch(self, *args, **kwargs):
        args = self.before_train_batch(args)
        kwargs = self.before_train_batch(kwargs)
        outputs = train_function(self, *args, **kwargs)
        outputs = self.after_train_batch(outputs)
        assert isinstance(outputs, dict)
        return outputs

    return _train_batch


@torch.no_grad()
def validate(validation_function):
    @wraps(validation_function)
    def _validate_batch(self, *args, **kwargs):
        args = self.before_validate_batch(args)
        kwargs = self.before_validate_batch(kwargs)
        outputs = validation_function(self, *args, **kwargs)
        outputs = self.after_validate_batch(outputs)
        assert isinstance(outputs, dict)
        return outputs

    return _validate_batch


@torch.no_grad()
def predict(predict_function):
    @wraps(predict_function)
    def _predict(self, *args, **kwargs):
        args = self.before_predict(args)
        kwargs = self.before_predict(kwargs)
        outputs = predict_function(self, *args, **kwargs)
        return outputs

    return _predict


# %% ../../nbs/capsule.ipynb 4
class Capsule(nn.Module):
    """
    Inherit from Capsule and train with fewer lines of code
    """

    def __init__(self, report=None):
        super().__init__()
        if report is not None:
            self.report = loaddill(report)

    # Train Utils
    def before_train_batch(self, data):
        self.train()
        self.optimizer.zero_grad()
        data = to(data, getattr(self, "device", "cuda"))
        return data

    def after_train_batch(self, outputs):
        outputs["loss"].backward()
        self.optimizer.step()
        return outputs

    # Validation Utils
    def before_validate_batch(self, data):
        self.eval()
        data = to(data, getattr(self, "device", "cuda"))
        return data

    def after_validate_batch(self, outputs):
        return outputs

    def before_predict(self, data):
        self.eval()
        data = to(data, getattr(self, "device", "cuda"))
        return data

    def after_predict(self, outputs):
        return outputs

    def load(self, weights_path=None, device="cpu"):
        if weights_path:
            load_torch_model_weights_to(self, weights_path, device=device)
        try:
            weights_path = weights_path + ".report"
            self.report = loaddill(weights_path)
        except:
            pass

    def save(self, save_to):
        if not exists(parent(save_to)):
            makedir(parent(save_to), prompt=False)
        save_torch_model_weights_from(self, save_to)
        if hasattr(self, "report"):
            save_to = save_to + ".report"
            dumpdill(self.report, save_to)

    # Fit function
    def fit(
        self,
        trn_dl=None,
        val_dl=None,
        num_epochs=1,
        lr=None,
        device="cuda",
        save_to=None,
        print_every=None,
        print_total=None,
        show_final_plot=True,
        **kwargs,
    ):
        if print_total:
            print_every = num_epochs // print_total

        if lr:
            for group in self.optimizer.param_groups:
                group["lr"] = lr
            Info(f"Learning Rate: {lr}")

        if not hasattr(self, "report"):
            self.report = Report(num_epochs, **kwargs)
        else:
            self.report = Report(num_epochs, old_report=self.report, **kwargs)

        self.device = device
        to(self, self.device)

        try:
            for epoch in range(num_epochs):
                self.report.n_epochs = num_epochs
                if trn_dl is not None:
                    N = len(trn_dl)
                    for ix, data in enumerate(trn_dl):
                        loss = self.train_batch(data)
                        self.report.record(pos=(epoch + (ix + 1) / N), **loss, end="\r")
                if val_dl is not None:
                    self.evaluate(
                        val_dl, report=self.report, device=device, epoch=epoch
                    )
                if (print_every and ((epoch + 1) % print_every == 0)) or epoch == 0:
                    self.report.report_avgs(epoch + 1)
                else:
                    self.report.report_avgs(epoch + 1, end="\r")
        except KeyboardInterrupt:
            pass

        if show_final_plot:
            self.report.plot(log=True, smooth=0)
        if save_to:
            self.save(save_to)
        self.report.finish_run(**kwargs)

    def evaluate(
        self, val_dl, report=None, device="cuda", epoch=None, show_report=False
    ):
        if report is None:
            report = Report(1)
            epoch = 0
            report_averages = True
        else:
            epoch = epoch
            report_averages = False
        self.device = device
        to(self, self.device)

        N = len(val_dl)
        for ix, data in enumerate(val_dl):
            loss = self.validate_batch(data)
            report.record(pos=(epoch + (ix + 1) / N), **loss, end="\r")

        avgs = report.report_avgs(1) if report_averages else None
        if show_report:
            report.plot(log=True, smooth=3)
        return avgs

    @train
    def train_batch(self, data):
        x, y = data
        _y = self(x)
        loss = self.criterion(_y, y)
        return {"loss": loss}

    @validate
    def validate_batch(self, data):
        x, y = data
        output = self(x)
        loss = self.criterion(output, y)
        return {"loss": loss}

    @predict
    def predict_batch(self, data):
        x, _ = data
        outputs = self(x)
        return outputs
